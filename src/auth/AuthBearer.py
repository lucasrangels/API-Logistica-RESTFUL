
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.AuthHandler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Falha na autenticação do esquema")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token de acesso inválido ou expirado")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Código de autorização inválido")

    def verify_jwt(self, jwt_token: str) -> bool:
        token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except:
            payload = None
        if payload:
            token_valid = True
        return token_valid