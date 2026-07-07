from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import create_tables
from routes import router

app = FastAPI(
    title="CIPHER",
    description="Central Intelligence Platform for Holdings and Executive Reporting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
app.include_router(router)

@app.get("/")
def root():
    return FileResponse("templates/home.html")

@app.get("/platform")
def platform():
    return FileResponse("templates/index.html")

@app.get("/connect")
def connect():
    return FileResponse("templates/connect.html")

@app.get("/health")
def health():
    return {"status": "healthy"}
