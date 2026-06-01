from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from routes.auth_routes import router as auth_router
from routes.horarios_routes import router as horarios_router
from routes.reservas_routes import router as reservas_router
from routes.avisos_routes import router as avisos_router

load_dotenv()

app = FastAPI(
    title="EuskoMove API",
    description="API REST para el servicio de autobuses EuskoMove",
    version="1.0.0",
)

# CORS — permite que el frontend se comunique con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia * por tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(horarios_router)
app.include_router(reservas_router)
app.include_router(avisos_router)

# Servir el frontend estático (opcional)
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")


@app.get("/")
def root():
    return {"mensaje": "EuskoMove API funcionando", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)