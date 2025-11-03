from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from src.pw_sistem.password_router import password_router

from src.utils.http_error_handler import http_error_handler

app = FastAPI()
bearer_shcema = HTTPBearer()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "https://kerberos-frontend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(http_error_handler)

app.title = "Kerberos AI Analyzer"

@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Kerberos AI Analyzer")

#Rutas
app.include_router(prefix="/passwords", router=password_router)


