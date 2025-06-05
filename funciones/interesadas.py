from typing import List, Optional
from uuid import UUID, uuid4
from services.supabase import supabase
from Schemas.Interesada import Interesada, InteresadaCreate

# Crear una interesada
def crear_interesada(data: InteresadaCreate) -> Interesada:
    interesada_dict = data.dict()
    interesada_dict["id"] = str(uuid4())
    result = supabase.table("interesada").insert(interesada_dict).execute()
    if not result.data:
        raise Exception("No se pudo crear la interesada")
    return Interesada(**result.data[0])

# Obtener todas las interesadas
def obtener_interesadas() -> List[Interesada]:
    result = supabase.table("interesada").select("*").execute()
    return [Interesada(**item) for item in result.data]

# Obtener una interesada por ID
def obtener_interesada_por_id(interesada_id: str) -> Optional[Interesada]:
    result = supabase.table("interesada").select("*").eq("id", interesada_id).single().execute()
    if not result.data:
        return None
    return Interesada(**result.data)

# Actualizar una interesada
def actualizar_interesada(interesada_id: str, data: InteresadaCreate) -> Optional[Interesada]:
    result = supabase.table("interesada").update(data.dict()).eq("id", interesada_id).execute()
    if not result.data:
        return None
    return Interesada(**result.data[0])

# Eliminar una interesada
def eliminar_interesada(interesada_id: str) -> bool:
    result = supabase.table("interesada").delete().eq("id", interesada_id).execute()
    return bool(result.data)
