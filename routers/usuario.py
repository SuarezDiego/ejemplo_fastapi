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


@router.post(
    "/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(database.get_db)
):
    """
    Crea un nuevo usuario en la base de datos.

    Verifica si ya existe un usuario con el mismo correo electrónico.
    Si no existe, se guarda el nuevo usuario y se retorna.

    Args:
        usuario (schemas.UsuarioCreate): Datos del usuario a crear.
        db (Session): Sesión de base de datos proporcionada por FastAPI.

    Returns:
        models.Usuario: El usuario recién creado.
    """
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


@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(database.get_db)):
    """
    Obtiene una lista de todos los usuarios en la base de datos.
    Args:
        db (Session): Sesión de base de datos proporcionada por FastAPI.
    Returns:
        List[models.Usuario]: Lista de usuarios.
    """
    return db.query(models.Usuario).all()


@router.get("/{id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(id: int, db: Session = Depends(database.get_db)):
    """
    Obtiene un usuario por su ID.
    Args:
        id (int): ID del usuario a obtener.
        db (Session): Sesión de base de datos proporcionada por FastAPI.
    Returns:
        models.Usuario: El usuario encontrado.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(
    id: int,
    usuario_update: schemas.UsuarioUpdate,
    db: Session = Depends(database.get_db)
):
    """
    Actualiza parcialmente un usuario existente.
    Args:
        id (int): ID del usuario a actualizar.
        usuario_update (schemas.UsuarioUpdate): Datos a actualizar.
        db (Session): Sesión de base de datos proporcionada por FastAPI.
    Returns:
        models.Usuario: El usuario actualizado.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for campo, valor in usuario_update.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id: int, db: Session = Depends(database.get_db)):
    """
    Elimina un usuario por su ID.
    Args:
        id (int): ID del usuario a eliminar.
        db (Session): Sesión de base de datos proporcionada por FastAPI.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return
