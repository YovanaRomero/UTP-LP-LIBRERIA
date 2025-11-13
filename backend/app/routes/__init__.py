from .categorias import router as categorias_router
from .productos import router as productos_router
from .clientes import router as clientes_router

__all__ = ["categorias_router", "productos_router", "clientes_router"]
