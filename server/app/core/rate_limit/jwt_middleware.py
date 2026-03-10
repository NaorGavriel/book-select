from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError

from app.core.config.config import settings


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request.state.jwt_payload = None

        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.startswith("Bearer "):
            print("auth_header exists")
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET,
                    algorithms=[settings.HASH_ALGORITHM]
                )
                print(payload)
                request.state.jwt_payload = payload

            except JWTError:
                # Invalid token -> treat as anonymous
                pass

        response = await call_next(request)
        return response