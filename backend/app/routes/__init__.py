from .categorias import router as categorias_router
from .productos import router as productos_router
from .clientes import router as clientes_router
from .usuarios import router as usuarios_router
from .pedidos import router as pedidos_router

__all__ = ["categorias_router", "productos_router", "clientes_router", "usuarios_router", "pedidos_router"]
