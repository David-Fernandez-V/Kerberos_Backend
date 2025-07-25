import src.models
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from src.routers.authentication_router import authentication_router
from src.routers.user_router import user_router
from src.routers.password_router import password_router
from src.routers.note_router import note_router
from src.routers.folder_router import folder_router
from src.routers.card_router import card_router

from src.utils.http_error_handler import http_error_handler

app = FastAPI()
bearer_shcema = HTTPBearer()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(http_error_handler)

app.title = "Kerberos API"

@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Kerberos API")

#Rutas
app.include_router(prefix="/authentication", router=authentication_router)
app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/passwords", router=password_router)
app.include_router(prefix="/folders", router=folder_router)
app.include_router(prefix="/notes", router=note_router)
app.include_router(prefix="/cards", router=card_router)


