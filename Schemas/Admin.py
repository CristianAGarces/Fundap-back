from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

class AdminCreate(BaseModel):
    nombre: str
    apellido: str
    email: str 
    telefono: str
    password: str 

class Admin(AdminCreate):
    id: UUID = Field(default_factory=uuid4)

class AdminLogin(BaseModel):
    email: str
    password: str