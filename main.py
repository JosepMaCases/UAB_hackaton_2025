from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

import pandas as pd
import os
from dotenv import load_dotenv

# 🔹 Nou: dependències per al chatbot
import requests
from pydantic import BaseModel

load_dotenv()

MAPTILER_API_KEY = os.getenv("MAPTILER_API_KEY")
if not MAPTILER_API_KEY:
    print("ALERTA: No s'ha trobat la MAPTILER_API_KEY al fitxer .env.")
    MAPTILER_API_KEY = ""

# 🔹 Nou: API KEY PublicAI per al chatbot
PUBLICAI_API_KEY = os.getenv("PUBLICAI_API_KEY")
if not PUBLICAI_API_KEY:
    print("ALERTA: No s'ha trobat PUBLICAI_API_KEY al .env. L'endpoint /chat no funcionarà.")

PUBLICAI_BASE_URL = "https://api.publicai.co/v1/chat/completions"
PUBLICAI_MODEL = "BSC-LT/salamandra-7b-instruct-tools-16k"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

START_LAT = 41.3874
START_LON = 2.1686
START_ZOOM = 12


def process_data():
    df = pd.read_csv("static/data/estacions.csv")

    # Tipus
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    df["PERSONA"] = pd.to_numeric(df["PERSONA"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")

    # Neteja mínima
    df = df.dropna(subset=["NOM_ESTACIO", "PERSONA", "lon", "lat"]).reset_index(drop=True)

    # Línies des de PICTO (L1, L3, L9S...)
    df["PICTO"] = df["PICTO"].fillna("").astype(str)
    df["LINIES"] = df["PICTO"].str.findall(r"L\d+S?")
    df["LINIES"] = df["LINIES"].apply(lambda xs: xs if xs and len(xs) > 0 else [])

    # Explosió línies per càlcul de mètriques
    df_linies = df.explode("LINIES").rename(columns={"LINIES": "LINIA"})
    df_linies = df_linies[df_linies["LINIA"].notna() & (df_linies["LINIA"] != "")]
    df_linies = df_linies.reset_index(drop=True)

    all_lines = sorted(df_linies["LINIA"].unique().tolist())

    # Top 10 estacions per volum total
    top_estacions = (
        df.groupby("NOM_ESTACIO")
        .agg(total_persones=("PERSONA", "sum"))
        .sort_values("total_persones", ascending=False)
        .head(10)
        .reset_index()
    )

    # Intercanviadors: estacions amb més d'una línia
    intercanviadors = (
        df.groupby("NOM_ESTACIO")
        .agg(
            total_persones=("PERSONA", "sum"),
            linies=("LINIES", lambda x: sorted(set(l for sub in x for l in sub)))
        )
        .reset_index()
    )

    intercanviadors["num_linies"] = intercanviadors["linies"].apply(len)
    intercanviadors = intercanviadors[intercanviadors["num_linies"] > 1].copy()
    intercanviadors["linies"] = intercanviadors["linies"].apply(lambda xs: ", ".join(xs))
    intercanviadors = intercanviadors.sort_values("total_persones", ascending=False).reset_index(drop=True)

    return df, df_linies, all_lines, top_estacions, intercanviadors


def compute_line_metrics(df_linies: pd.DataFrame) -> pd.DataFrame:
    line_stats = (
        df_linies
        .groupby("LINIA")
        .agg(
            num_parades=("NOM_ESTACIO", "nunique"),
            total_persones=("PERSONA", "sum"),
        )
        .reset_index()
    )

    line_stats["mitjana_per_parada"] = (
        line_stats["total_persones"] / line_stats["num_parades"]
    )

    return line_stats.sort_values("total_persones", ascending=False)


# Pre-càlcul global
DF, DF_LINIES, ALL_LINES, TOP_ESTACIONS_DF, INTERCANVIADORS_DF = process_data()
LINE_STATS_DF = compute_line_metrics(DF_LINIES)

# KPIs globals
TOTAL_PASSATGERS = int(DF["PERSONA"].sum())
MITJANA_PASSATGERS = float(DF["PERSONA"].mean())
NUM_ESTACIONS = int(DF["NOM_ESTACIO"].nunique())
NUM_LINIES = len(ALL_LINES)

# Per Jinja
LINE_STATS = LINE_STATS_DF.to_dict(orient="records")
TOP_ESTACIONS = TOP_ESTACIONS_DF.to_dict(orient="records")
INTERCANVIADORS = INTERCANVIADORS_DF.to_dict(orient="records")

# Nou: CSV com a context per al chatbot
# Si és molt gran, el limitem una mica per no rebentar tokens.
CSV_FOR_BOT = DF.to_csv(index=False)

# Opcional: si vols ser paranoic amb el límit de tokens:
MAX_CHARS = 15000
if len(CSV_FOR_BOT) > MAX_CHARS:
    # Mostra totes les columnes però només una mostra d’estacions
    CSV_FOR_BOT = DF.sample(n=min(len(DF), 200), random_state=42).to_csv(index=False)


# =========================
# RUTES EXISTENTS
# =========================

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "start_lat": START_LAT,
            "start_lon": START_LON,
            "start_zoom": START_ZOOM,
            "maptiler_api_key": MAPTILER_API_KEY,
        },
    )


@app.get("/map")
def map_view(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "start_lat": START_LAT,
            "start_lon": START_LON,
            "start_zoom": START_ZOOM,
            "maptiler_api_key": MAPTILER_API_KEY,
        },
    )


@app.get("/ampliacions")
def ampliacions_view(request: Request):
    return templates.TemplateResponse(
        "ampliacions.html",
        {
            "request": request,
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(request: Request):
    line_labels = [row["LINIA"] for row in LINE_STATS]
    line_totals = [int(row["total_persones"]) for row in LINE_STATS]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_passatgers": TOTAL_PASSATGERS,
            "mitjana_passatgers": MITJANA_PASSATGERS,
            "num_estacions": NUM_ESTACIONS,
            "num_linies": NUM_LINIES,
            "line_stats": LINE_STATS,
            "line_labels": line_labels,
            "line_totals": line_totals,
            "top_estacions": TOP_ESTACIONS,
            "intercanviadors": INTERCANVIADORS,
        },
    )


# =========================
# 🔹 PART NOVA: CHATBOT
# =========================

class ChatRequest(BaseModel):
    message: str
    history: list[dict] | None = None  # [{ "role": "user"/"assistant", "content": "..." }, ...]


def ask_salamandra(messages, max_tokens: int = 512, temperature: float = 0.4) -> str:
    """
    Fa una crida al model Salamandra via PublicAI.
    """
    if not PUBLICAI_API_KEY:
        # No trenquem tot el servei, només el xat
        return "Error de configuració: falta la PUBLICAI_API_KEY al servidor."

    headers = {
        "Authorization": f"Bearer {PUBLICAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": PUBLICAI_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        resp = requests.post(PUBLICAI_BASE_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error amb PublicAI:", e)
        return "Hi ha hagut un error en comunicar amb el model. Revisa la configuració del servidor."

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    Endpoint REST perquè el front demani respostes del chatbot.
    El model rep també el CSV de les dades SmartMetro com a context.
    """
    system_prompt = (
        "Ets l'assistent SmartMetro. "
        "Respon SEMPRE en català. "
        "Tens accés al conjunt de dades SmartMetro en format CSV, amb informació sobre estacions, "
        "nombre de persones usuàries, línies i coordenades. "
        "Fes servir EXPLÍCITAMENT aquestes dades per respondre preguntes sobre: estacions més transitades, "
        "intercanviadors, volum per línia, etc. "
        "Si alguna cosa no surt a les dades, digues-ho clarament. "
        "Aquí tens el dataset complet (o una mostra representativa si és massa llarg):\n\n"
        f"{CSV_FOR_BOT}\n\n"
        "Quan responguis, explica els resultats de forma entenedora i, si cal, esmenta noms d'estacions, línies "
        "i valors aproximats basats en aquest CSV."
    )

    messages = [{"role": "system", "content": system_prompt}]

    if req.history:
        for m in req.history:
            role = m.get("role")
            content = m.get("content")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": req.message})

    reply = ask_salamandra(messages)
    return {"reply": reply}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
