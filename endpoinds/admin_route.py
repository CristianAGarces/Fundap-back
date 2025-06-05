from fastapi import APIRouter, HTTPException, Depends
from middlewares.jwt import JWTBearer
from Schemas.Admin import Admin, AdminCreate, AdminLogin
from funciones import admin as admin_db
from funciones.login import create_token
from funciones.email_utils import send_admin_confirmation_email
from funciones.admin_confirm_tokens import admin_confirmation_tokens
import uuid
from typing import List

router = APIRouter()

# # Crear un admin
# @router.post("/", response_model=Admin)
# def crear_admin(admin: AdminCreate):
#     try:
#         return admin_db.crear_admin(admin)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Obtener todos los admins
@router.get("/", response_model=List[Admin], dependencies=[Depends(JWTBearer())])
def obtener_admins():
    try:
        return admin_db.obtener_admins()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un admin por ID
@router.get("/{admin_id}", response_model=Admin, dependencies=[Depends(JWTBearer())])
def obtener_admin_por_id(admin_id: str):
    try:
        admin_obj = admin_db.obtener_admin_por_id(admin_id)
        if admin_obj is None:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
        return admin_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Eliminar un admin
@router.delete("/{admin_id}")
def eliminar_admin(admin_id: str):
    try:
        ok = admin_db.eliminar_admin(admin_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
        return {"mensaje": "Admin eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar un admin
@router.put("/{admin_id}", response_model=Admin)
def actualizar_admin(admin_id: str, admin: AdminCreate):
    try:
        actualizado = admin_db.actualizar_admin(admin_id, admin)
        if actualizado is None:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
        return actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de login para admin
@router.post("/login")
def login_admin(login_data: AdminLogin):
    try:
        admin = admin_db.obtener_admin_por_email(login_data.email)
        if not admin:
            raise HTTPException(status_code=401, detail="No existe una cuenta con esos datos.")
        if admin.password != login_data.password:
            raise HTTPException(status_code=401, detail="El correo o la contraseña son incorrectos.")
        confirm_token = str(uuid.uuid4())
        admin_confirmation_tokens[confirm_token] = admin.email
        send_admin_confirmation_email(admin.email, confirm_token)
        return {"mensaje": "Se ha enviado un correo de confirmación. Por favor revisa tu email para continuar."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado, estos datos NO existen. Intenta nuevamente o contacta soporte.")

# Endpoint para confirmar acceso de admin
@router.get("/confirm-access/{token}")
def confirm_admin_access(token: str):
    email = admin_confirmation_tokens.pop(token, None)
    if not email:
        raise HTTPException(status_code=400, detail="Token de confirmación inválido o expirado")
    admin = admin_db.obtener_admin_por_email(email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    # Generar token JWT
    jwt_token = create_token({"email": admin.email, "nombre": admin.nombre, "apellido": admin.apellido, "id": str(admin.id)})
    return {"mensaje": "Acceso confirmado", "token": jwt_token, "admin": {"nombre": admin.nombre, "apellido": admin.apellido, "email": admin.email}}
