from fastapi import FastAPI
import models
import database
from routers.usuario import router as usuario_router

app = FastAPI()

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

# Incluir router
app.include_router(usuario_router)
