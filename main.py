from fastapi import FastAPI, Request, Depends, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form, Request
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # monta la carpeta static per servir fitxers estatics

templates = Jinja2Templates(directory="templates")  # carpeta on hi ha les plantilles jinja2

START_LAT = 41.3874
START_LON = 2.1686
START_ZOOM = 12

@app.get("/")
def index(request: Request):

    return templates.TemplateResponse("index2.html", {
        "request": request,
        "start_lat": START_LAT,
        "start_lon": START_LON,
        "start_zoom": START_ZOOM
    })


@app.get("/map")
def map_view(request: Request):

    return templates.TemplateResponse("map.html", {
        "request": request
    }) 


@app.get("/dashboard")
def dashboard_view(request: Request):

    return templates.TemplateResponse("dashboard.html", {
        "request": request
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)