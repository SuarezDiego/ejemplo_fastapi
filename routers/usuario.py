from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import database


router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


# Crear usuario
@router.post(
    "/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(database.get_db)
):
    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=400, detail="El email ya está registrado")
    nuevo_usuario = models.Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# Obtener todos los usuarios
@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(database.get_db)):
    return db.query(models.Usuario).all()


# Obtener usuario por ID
@router.get("/{id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(id: int, db: Session = Depends(database.get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Actualizar parcialmente usuario (PATCH)
@router.patch("/{id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(
    id: int,
    usuario_update: schemas.UsuarioUpdate,
    db: Session = Depends(database.get_db)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for campo, valor in usuario_update.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario


# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id: int, db: Session = Depends(database.get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return
