# Libreria Virtual 1.0.0
![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)

## 🚀 Acerca del grupo
- Romero Gutierrez Yovana

## :hammer:Funcionalidades del proyecto
- `Mantenimiento de Categoria`: 
  
| Field                     | Type     | Description      |
| :------------------------ | :------- | :--------------- |
| `categoria_id`            | `integer` | **Required**. primary key  |
| `categoria_nombre`        | `string` | nombre de categoria |
| `categoria_descripcion`   | `string` | descripcion de categoria |
  

 Permite mostrar la información de las categorías, así como las operaciones:
    - Buscar categoría
    - Registrar categoría
    - Modificar categoría
    - Eliminar categoría 

- `Mantenimiento de Productos`: 
  
| Field                     | Type     | Description      |
| :------------------------ | :------- | :--------------- |
| `producto_id`             | `string` | **Required**. primary key  |
| `producto_nombre`         | `string` | nombre de producto         |
| `producto_descripcion`    | `string` | descripcion de producto    |
| `producto_precio`         | `decimal` | precio de producto        |
| `producto_stock`          | `integer` | stock de producto         |
| `categoria_id`            | `integer` | **Required**. foreign key categoria     |
| `producto_color`          | `string` | color de producto          |
| `producto_dimensiones`    | `string` | dimensiones de producto    |

Permite mostrar la información de los productos, así como las operaciones:
  - Buscar Producto
  - Registrar Producto
  - Modificar Producto
  - Eliminar Producto 
  - Asignar productos a categorías


## 🛠️ Ejecutar el proyecto
Muestra las instrucciones necesarias para clonar y ejecutar el proyecto

### Clonar repositorio
considere siempre usar la rama: **master**

```bash
git clone https://github.com/YovanaRomero/UTP-LP-LIBRERIA.git
```
### BackEnd
ubiquese desde su terminal en la carpeta del proyecto `backend`

#### Purgar dependencias 

```shell
pip cache purge
```

#### Instalar dependencias 

```shell
pip install -r requirements.txt
```
#### Ejecutar desde la terminal
```shell
uvicorn app.main:app --reload
```
#### Ejecutar desde Visual Code
Configurar un launch.json
Ve al panel "Run and Debug" (icono de play y bug en la barra lateral).

#### Swagger
> Nota: verifique ingresando a   `http://localhost:8000/docs` 

![Texto alternativo](testing/screenshot/screenshot_swagger.png).

## License

[MIT](https://choosealicense.com/licenses/mit/)




