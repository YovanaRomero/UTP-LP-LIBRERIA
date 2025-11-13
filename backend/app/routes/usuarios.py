from fastapi import APIRouter, HTTPException, status
from ..models import UsuarioLogin, TokenResponse
from ..services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: UsuarioLogin):
    """
    Endpoint de autenticación.
    Retorna un JWT token con información del usuario en los claims.
    
    Ejemplo de request:
    ```json
    {
      "usuario_nombre": "admin",
      "usuario_password": "password123"
    }
    ```
    
    Ejemplo de response:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "usuario_id": 1,
      "usuario_nombre": "admin",
      "usuario_descripcion": "Administrador del sistema"
    }
    ```
    """
    resultado = UsuarioService.autenticar_usuario(login_data)
    
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos"
        )
    
    return resultado
