from typing import List, Optional
from uuid import UUID, uuid4
from services.supabase import supabase
from Schemas.Admin import Admin, AdminCreate

# # Crear un admin
# def crear_admin(data: AdminCreate) -> Admin:
#     admin_dict = data.dict()
#     admin_dict["id"] = str(uuid4())
#     result = supabase.table("admin").insert(admin_dict).execute()
#     if not result.data:
#         raise Exception("No se pudo crear el admin")
#     return Admin(**result.data[0])

# Obtener todos los admins
def obtener_admins() -> List[Admin]:
    result = supabase.table("admin").select("*").execute()
    return [Admin(**item) for item in result.data]

# Obtener un admin por ID
def obtener_admin_por_id(admin_id: str) -> Optional[Admin]:
    result = supabase.table("admin").select("*").eq("id", admin_id).single().execute()
    if not result.data:
        return None
    return Admin(**result.data)

# Obtener un admin por email
def obtener_admin_por_email(email: str) -> Optional[Admin]:
    result = supabase.table("admin").select("*").eq("email", email).single().execute()
    if not result.data:
        return None
    return Admin(**result.data)

# Actualizar un admin
def actualizar_admin(admin_id: str, data: AdminCreate) -> Optional[Admin]:
    result = supabase.table("admin").update(data.dict()).eq("id", admin_id).execute()
    if not result.data:
        return None
    return Admin(**result.data[0])

# Eliminar un admin
def eliminar_admin(admin_id: str) -> bool:
    result = supabase.table("admin").delete().eq("id", admin_id).execute()
    return bool(result.data)
