from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()

# STATIC
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# TEMPLATES
templates = Jinja2Templates(directory="app/templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

stages = [
    {
        "id": "1001",
        "secuencia": "1",
        "camion": "E45-1",
        "avance": 25,
        "estado": "Cargando"
    },
    {
        "id": "1002",
        "secuencia": "2",
        "camion": "E46-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1003",
        "secuencia": "3",
        "camion": "E47-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1004",
        "secuencia": "4",
        "camion": "E48-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1005",
        "secuencia": "5",
        "camion": "E49-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1006",
        "secuencia": "6",
        "camion": "E50-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1007",
        "secuencia": "7",
        "camion": "E51-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1008",
        "secuencia": "8",
        "camion": "E52-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1009",
        "secuencia": "9",
        "camion": "E53-1",
        "avance": 70,
        "estado": "En Proceso"
    },
    {
        "id": "1010",
        "secuencia": "10",
        "camion": "E54-1",
        "avance": 70,
        "estado": "En Proceso"
    }
]

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="app.html"
)

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )   


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    global stages

    await websocket.accept()

    clients.append(websocket)

    # enviar estado actual al conectarse
    await websocket.send_json(stages)

    try:

        while True:

            data = await websocket.receive_json()

            stages = data

            # reenviar a TODOS
            for client in clients:
                await client.send_json(stages)

    except WebSocketDisconnect:

        clients.remove(websocket)