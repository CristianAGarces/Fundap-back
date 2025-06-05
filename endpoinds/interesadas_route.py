from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError
from Schemas.Interesada import Interesada, InteresadaCreate
from funciones import interesadas as interesadas_db
from typing import List
from middlewares.jwt import JWTBearer

router = APIRouter()

# Crear una interesada
@router.post("/", response_model=Interesada)
def crear_interesada(interesada: InteresadaCreate):
    try:
        # Validación adicional para el número de documento
        if not interesada.numero_documento.isdigit() or not (5 <= len(interesada.numero_documento) <= 15):
            return JSONResponse(
                status_code=422,
                content={
                    "mensaje": "El número de documento debe contener solo dígitos y tener entre 5 y 15 caracteres."
                }
            )
        return interesadas_db.crear_interesada(interesada)
    except Exception as e:
        # Manejo específico para error de email duplicado
        if hasattr(e, 'args') and e.args and 'duplicate key value violates unique constraint' in str(e.args[0]):
            return JSONResponse(
                status_code=409,
                content={
                    "mensaje": "El correo electrónico ya está registrado. Por favor usa otro correo."
                }
            )
        raise HTTPException(status_code=500, detail=f"Error interno al crear interesada: {str(e)}")

# Obtener todas las interesadas
@router.get("/", response_model=List[Interesada], dependencies=[Depends(JWTBearer())])
def obtener_interesadas():
    try:
        return interesadas_db.obtener_interesadas()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al obtener interesadas: " + str(e))

# Obtener una interesada por ID
@router.get("/{interesada_id}", response_model=Interesada)
def obtener_interesada_por_id(interesada_id: str):
    try:
        interesada = interesadas_db.obtener_interesada_por_id(interesada_id)
        if interesada is None:
            raise HTTPException(status_code=404, detail="Interesada no encontrada")
        return interesada
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al buscar interesada: " + str(e))

# Eliminar una interesada
@router.delete("/{interesada_id}")
def eliminar_interesada(interesada_id: str):
    try:
        ok = interesadas_db.eliminar_interesada(interesada_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Interesada no encontrada")
        return {"mensaje": "Interesada eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al eliminar interesada: " + str(e))

# Actualizar una interesada
@router.put("/{interesada_id}", response_model=Interesada)
def actualizar_interesada(interesada_id: str, interesada: InteresadaCreate):
    try:
        actualizada = interesadas_db.actualizar_interesada(interesada_id, interesada)
        if actualizada is None:
            raise HTTPException(status_code=404, detail="Interesada no encontrada")
        return actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al actualizar interesada: " + str(e))
