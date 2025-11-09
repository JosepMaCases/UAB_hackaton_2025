from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
MAPTILER_API_KEY = os.getenv("MAPTILER_API_KEY")

if not MAPTILER_API_KEY:
    print("ALERTA: No s'ha trobat la MAPTILER_API_KEY al fitxer .env.")
    MAPTILER_API_KEY = ""

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
    df["LINIES"] = df["PICTO"].str.findall(r"L\d+S?")  # L1, L5, L9S, L10S

    df["LINIES"] = df["LINIES"].apply(lambda xs: xs if xs and len(xs) > 0 else None)

    # Explosió línies
    df_linies = df.explode("LINIES").rename(columns={"LINIES": "LINIA"})
    df_linies = df_linies[df_linies["LINIA"].notna()].reset_index(drop=True)

    all_lines = sorted(df_linies["LINIA"].unique().tolist())

    return df, df_linies, all_lines


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

    # Ordenat per volum
    line_stats = line_stats.sort_values("total_persones", ascending=False)

    return line_stats


# Pre-càlcul global
DF, DF_LINIES, ALL_LINES = process_data()
LINE_STATS_DF = compute_line_metrics(DF_LINIES)

# KPIs globals
TOTAL_PASSATGERS = int(DF["PERSONA"].sum())
MITJANA_PASSATGERS = float(DF["PERSONA"].mean())
NUM_ESTACIONS = int(DF["NOM_ESTACIO"].nunique())
NUM_LINIES = len(ALL_LINES)

# Per enviar al template: ho passem ja com a llista de dicts
LINE_STATS = LINE_STATS_DF.to_dict(orient="records")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "start_lat": START_LAT,
            "start_lon": START_LON,
            "start_zoom": START_ZOOM,
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
        },
    )


@app.get("/ampliacions")
def map_view(request: Request):
    return templates.TemplateResponse(
        "ampliacions.html",
        {
            "request": request,
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(request: Request):
    # KPIs globals ja calculats abans
    line_stats = LINE_STATS  # llista de dicts

    line_labels = [row["LINIA"] for row in line_stats]
    line_totals = [int(row["total_persones"]) for row in line_stats]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_passatgers": TOTAL_PASSATGERS,
            "mitjana_passatgers": MITJANA_PASSATGERS,
            "num_estacions": NUM_ESTACIONS,
            "num_linies": NUM_LINIES,
            "line_stats": line_stats,
            "line_labels": line_labels,
            "line_totals": line_totals,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
