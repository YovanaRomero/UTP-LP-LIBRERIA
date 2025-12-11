from ..models import Producto, ProductoCreate, ProductoUpdate
from ..repositories import ProductoRepository
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
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

# SE GENERA EL REPORTE DE LOS PRODUCTOS EN EXCEL
    @staticmethod
    def generar_excel_productos():
        #Se llama al repositorio para obtener los datos de la  base de datos,
        #devolviendo una lista de objetos Pydantic
        productos = ProductoRepository.get_all()
        #Se valida si existen productos, de lo contrario no genera ningun excel
        if not productos:
            return None

        # Convierte cada objeto en Pydantic en un Diccionario.
        data = [p.dict() for p in productos]

        # Crear DataFrame con pandas con la informacion de los productos
        # Este dataframe sera la base de datos de excel
        df = pd.DataFrame(data)

        # Crear Excel en memoria
        output = io.BytesIO()
        #Pandas escribe el dataframe dentro de un archivo excel
        #con el nombre de Productos
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Productos")

        output.seek(0)
        #finalmente devuelve el archivo excel para enviarlo al frontend
        return output