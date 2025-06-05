from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from funciones.login import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        # Permitir cualquier admin válido (no restringir por email)
        # Si quieres lógica extra, puedes agregarla aquí
        return auth