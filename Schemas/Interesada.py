from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional, Literal

class InteresadaCreate(BaseModel):
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    telefono: str = Field(..., max_length=10)
    mensaje: str = Field(..., max_length=50)
    type_document: Literal['CC', 'TI', 'CE', 'PP', 'RC', 'NIT', 'OTRO']
    numero_documento: str = Field(..., max_length=15)

    def __init__(self, **data):
        if 'nombre' in data:
            data['nombre'] = ' '.join([w.capitalize() for w in data['nombre'].split()])
        if 'apellido' in data:
            data['apellido'] = ' '.join([w.capitalize() for w in data['apellido'].split()])
        super().__init__(**data)

class Interesada(InteresadaCreate):
    id: UUID = Field(default_factory=uuid4)