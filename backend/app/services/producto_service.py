from ..models import Producto, ProductoCreate, ProductoUpdate
from ..repositories import ProductoRepository
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io

class ProductoService:
    """Servicio de lógica de negocio para productos."""

    @staticmethod
    def get_all_productos():
        """Obtener todos los productos."""
        return ProductoRepository.get_all()

    @staticmethod
    def get_producto_by_id(producto_id: int):
        """Obtener un producto por ID."""
        return ProductoRepository.get_by_id(producto_id)

    @staticmethod
    def create_producto(producto: ProductoCreate):
        """Crear un nuevo producto."""
        return ProductoRepository.create(producto)

    @staticmethod
    def update_producto(producto_id: int, producto: ProductoUpdate):
        """Actualizar un producto existente."""
        return ProductoRepository.update(producto_id, producto)

    @staticmethod
    def delete_producto(producto_id: int):
        """Eliminar un producto."""
        return ProductoRepository.delete(producto_id)


# NUEVAS FUNCIONES DE STOCK Y GRÁFICO

    @staticmethod
    def obtener_stock_productos():
        """Retorna stock como JSON."""
        return ProductoRepository.get_stock_productos()
# AQUI SE GENERA LA IMAGEN DE STOCK POR PRODUCTO
    @staticmethod
    def generar_grafico_stock():
        productos = ProductoRepository.get_all()
        nombres = [p.producto_nombre for p in productos]
        stock = [p.producto_stock for p in productos]

        fig, ax = plt.subplots(figsize=(10, 6))
        barras = ax.barh(nombres, stock, color='skyblue')
        
        # Agregar valores en cada barra
        for i, barra in enumerate(barras):
            ancho = barra.get_width()
            ax.text(ancho, barra.get_y() + barra.get_height()/2, 
                   f' {int(ancho)}', 
                   ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel("Stock", fontsize=12, fontweight='bold', labelpad=10)
        ax.set_ylabel("Productos", fontsize=12, fontweight='bold', labelpad=10)
        ax.set_title("Análisis de Stock de Productos (Matplotlib)", fontsize=20, fontweight='bold', pad=20)
        plt.tight_layout()
# SE GENERA EN FORMATO PNG
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf
