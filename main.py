from typing import Union
from endpoinds import interesadas_route, admin_route
from fastapi import FastAPI, HTTPException, Request
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Include the routes from the 'interesadas_route' module
app.include_router(interesadas_route.router, prefix="/interesadas", tags=["interesadas"])
app.include_router(admin_route.router, prefix="/admin", tags=["admin"])

@app.get("/")
def read_root():
    return {"Hello": "World 🌎 this is fastApi"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Endpoint de testeo
@app.get("/test")
def test_connection():
    try:
        from services.supabase import supabase
        response = supabase.table("Interesadas").select("*").limit(1).execute()
        return {
            "estado": "conectado ✅",
            "tabla": "pqrs",
            "datos_de_prueba": response.data
        }
    except Exception as e:
        return {"estado": "error ❌", "detalle": str(e)}

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    errores = []
    for err in exc.errors():
        errores.append({
            "campo": err.get("loc", [])[1:] if len(err.get("loc", [])) > 1 else err.get("loc", []),
            "mensaje": err.get("msg", "Error de validación")
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "mensaje": "Datos ingresados no válidos. Por favor revisa los campos.",
            "errores": errores
        },
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    # Siempre devolver ambos campos para el frontend
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "mensaje": exc.detail
        },
    )

@app.get("/favicon.ico")
def favicon():
    from fastapi.responses import Response
    return Response(content="", media_type="image/x-icon")

# Arranque
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

origins = [
    "https://fundap-front.netlify.app",  # tu frontend en producción
    "http://localhost:3000",             # para desarrollo local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)