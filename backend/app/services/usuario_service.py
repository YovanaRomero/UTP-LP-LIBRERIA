from ..models import Usuario, UsuarioLogin, TokenResponse
from ..repositories import UsuarioRepository
from datetime import datetime, timedelta
from typing import Optional
import jwt
import json

# Configuración JWT
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"  # CAMBIAR EN PRODUCCIÓN
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UsuarioService:
    """Servicio de autenticación y lógica de negocio para usuarios."""

    @staticmethod
    def generar_token_jwt(usuario_id: int, usuario_nombre: str, usuario_descripcion: Optional[str] = None) -> str:
        """
        Generar un JWT con información del usuario en los claims.
        
        Claims incluyen:
        - sub: usuario_id
        - usuario_nombre: nombre del usuario
        - usuario_descripcion: descripción del usuario
        - exp: tiempo de expiración
        - iat: issued at
        """
        payload = {
            "sub": str(usuario_id),
            "usuario_nombre": usuario_nombre,
            "usuario_descripcion": usuario_descripcion,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def verificar_contraseña(contraseña_plana: str, contraseña_almacenada: str) -> bool:
        """
        Verificar contraseña. Actualmente usa comparación simple.
        
        IMPORTANTE: Para producción, descomenta las líneas de passlib y bcrypt:
        
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(contraseña_plana, contraseña_almacenada)
        """
        # Comparación simple (no segura) - SOLO PARA DESARROLLO
        return contraseña_plana == contraseña_almacenada
        
        # Descomenta esto en producción (requiere: pip install passlib bcrypt)
        # from passlib.context import CryptContext
        # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # return pwd_context.verify(contraseña_plana, contraseña_almacenada)

    @staticmethod
    def autenticar_usuario(login: UsuarioLogin) -> Optional[TokenResponse]:
        """
        Autenticar usuario con nombre y contraseña.
        Retorna TokenResponse con JWT si autenticación es exitosa.
        """
        # Buscar usuario por nombre
        usuario_data = UsuarioRepository.get_by_nombre(login.usuario_nombre)
        
        if not usuario_data:
            return None  # Usuario no existe
        
        # Verificar contraseña
        if not UsuarioService.verificar_contraseña(login.usuario_password, usuario_data["usuario_password"]):
            return None  # Contraseña incorrecta
        
        # Verificar estado (opcional: si usuario_estado != 1, rechazar)
        if usuario_data.get("usuario_estado") != 1:
            return None  # Usuario inactivo
        
        # Generar JWT
        token = UsuarioService.generar_token_jwt(
            usuario_id=usuario_data["usuario_id"],
            usuario_nombre=usuario_data["usuario_nombre"],
            usuario_descripcion=usuario_data["usuario_descripcion"]
        )
        
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            usuario_id=usuario_data["usuario_id"],
            usuario_nombre=usuario_data["usuario_nombre"],
            usuario_descripcion=usuario_data["usuario_descripcion"]
        )

    @staticmethod
    def decodificar_token(token: str) -> Optional[dict]:
        """
        Decodificar y validar un JWT.
        Retorna el payload si es válido, None si es inválido.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
