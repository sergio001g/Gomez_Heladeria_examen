# FrostBite API - Heladería REST API

Backend API REST completo para la gestión de sabores y productos de heladería FrostBite, con implementación de JWT Authentication, descuento por volumen y planificación de producción.

## Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- pip/venv

## Instalación

### 1. Clonar el repositorio

```bash
cd /home/alumnos/Documents/heladeria_api
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

El archivo `.env` ya contiene la configuración necesaria:

```
DEBUG=1
SECRET_KEY=dev-secret-key
DB_NAME=heladeria_db
DB_USER=heladeria_user
DB_PASSWORD=admin123
DB_HOST=127.0.0.1
DB_PORT=5432
CORS_ORIGIN=http://localhost:5173
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (ya creado)

Usuario: `admin`
Contraseña: `admin123`

### 7. Ejecutar servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

El servidor estará disponible en: `http://localhost:8000`

## Endpoints Disponibles

### Autenticación

- `POST /api/auth/register/` - Registrar nuevo usuario
- `POST /api/auth/login/` - Obtener tokens JWT
- `POST /api/auth/refresh/` - Refrescar token de acceso

### Sabores (CRUD)

- `GET /api/sabores/` - Listar sabores (público)
- `POST /api/sabores/` - Crear sabor (solo staff)
- `GET /api/sabores/{id}/` - Obtener sabor (público)
- `PUT /api/sabores/{id}/` - Actualizar sabor (solo staff)
- `DELETE /api/sabores/{id}/` - Eliminar sabor (solo staff)
- `GET /api/sabores/?search=nombre` - Buscar sabores

### Productos (CRUD)

- `GET /api/productos/` - Listar productos (público)
- `POST /api/productos/` - Crear producto (solo staff)
- `GET /api/productos/{id}/` - Obtener producto (público)
- `PUT /api/productos/{id}/` - Actualizar producto (solo staff)
- `DELETE /api/productos/{id}/` - Eliminar producto (solo staff)
- `GET /api/productos/?sabor=1` - Filtrar por sabor
- `GET /api/productos/?disponible=true` - Filtrar por disponibilidad
- `GET /api/productos/?search=nombre` - Buscar por nombre o código
- `GET /api/productos/?ordering=precio_venta` - Ordenar por precio

### Pedidos (Descuento por Volumen)

- `POST /api/pedido/` - Calcular pedido con descuento automático

**Request:**
```json
[
  {
    "nombre": "Chocolate",
    "precio": 2.50,
    "cantidad": 3
  }
]
```

**Response:**
```json
{
  "total_unidades": 3,
  "subtotal": 7.50,
  "descuento_pct": 0,
  "total": 7.50,
  "detalle": [
    {
      "nombre": "Chocolate",
      "cantidad": 3,
      "subtotal_linea": 7.50
    }
  ]
}
```

**Tabla de Descuentos:**
- 1-3 unidades: 0%
- 4-6 unidades: 10%
- 7-10 unidades: 15%
- Más de 10: 20%

### Producción (Planificación WHILE)

- `GET /api/produccion/?presupuesto=20&costos=4.5,3.0,6.0,5.5,4.0` - Calcular producción

**Query Parameters:**
- `presupuesto` (float): Presupuesto total disponible
- `costos` (string): Lista de costos separados por comas

**Response:**
```json
{
  "productos_producidos": 3,
  "presupuesto_gastado": 13.50,
  "presupuesto_restante": 6.50,
  "detalle": [
    {
      "producto_numero": 1,
      "costo": 4.50
    },
    {
      "producto_numero": 2,
      "costo": 3.00
    },
    {
      "producto_numero": 3,
      "costo": 6.00
    }
  ]
}
```

## Modelos

### Sabor

```python
- id (int): Identificador único
- nombre (str): Nombre del sabor (único, máx 120 caracteres)
```

### Producto

```python
- id (int): Identificador único
- sabor (ForeignKey): Referencia a Sabor
- nombre (str): Nombre del producto (máx 120 caracteres)
- codigo (str): Código único del producto
- precio_venta (decimal): Precio de venta
- costo_insumos (decimal): Costo de insumos
- disponible (bool): Estado de disponibilidad
```

## Permisos

- `GET`: Público (no requiere autenticación)
- `POST/PUT/PATCH/DELETE`: Solo usuarios staff (requiere JWT)

## Autenticación JWT

Incluir el token en el header de las peticiones protegidas:

```
Authorization: Bearer <access_token>
```

## Postman Collection

Importar `FrostBite.postman_collection.json` en Postman para tener todos los endpoints preconfigurados.

**Variables de Postman:**
- `{{base_url}}` = http://localhost:8000
- `{{access_token}}` = Token obtenido del login
- `{{refresh_token}}` = Token de refresco

## Admin Panel

Acceder a `http://localhost:8000/admin/` con usuario `admin` y contraseña `admin123`

## Estructura del Proyecto

```
heladeria_api/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── admin.py
│   └── migrations/
├── venv/
├── manage.py
├── .env
├── requirements.txt
└── README.md
```

## Datos Iniciales

La base de datos se carga con 5 sabores y 10 productos de ejemplo.

## Troubleshooting

### Error de conexión a PostgreSQL

Verificar que PostgreSQL está corriendo:
```bash
pg_isready -h 127.0.0.1 -p 5432
```

Verificar credenciales en `.env`:
```bash
PGPASSWORD='admin123' psql -h 127.0.0.1 -U heladeria_user -d heladeria_db -c "SELECT 1;"
```

### Error de módulos no encontrados

Asegurar que el virtualenv está activado:
```bash
source venv/bin/activate
```

### Limpiar migraciones (desarrollo)

```bash
python manage.py migrate catalog zero
rm catalog/migrations/0*.py
```

## Licencia

MIT

## Autor

FrostBite Heladería API
