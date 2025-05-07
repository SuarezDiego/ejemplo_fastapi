from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    contraseña: str


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        orm_mode = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
