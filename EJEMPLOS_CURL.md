# Ejemplos de Peticiones a la API FrostBite

## Variables

```
BASE_URL=http://localhost:8000
```

## 1. Autenticación

### Registrar usuario

```bash
curl -X POST $BASE_URL/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepass123"
  }'
```

### Login (obtener tokens)

```bash
curl -X POST $BASE_URL/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refrescar token

```bash
curl -X POST $BASE_URL/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

## 2. Sabores

### Listar sabores

```bash
curl $BASE_URL/api/sabores/
```

### Crear sabor (requiere autenticación staff)

```bash
ACCESS_TOKEN="YOUR_ACCESS_TOKEN"

curl -X POST $BASE_URL/api/sabores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "nombre": "Pistache"
  }'
```

### Obtener sabor específico

```bash
curl $BASE_URL/api/sabores/1/
```

### Actualizar sabor

```bash
curl -X PUT $BASE_URL/api/sabores/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "nombre": "Chocolate Belga"
  }'
```

### Eliminar sabor

```bash
curl -X DELETE $BASE_URL/api/sabores/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Buscar sabores

```bash
curl "$BASE_URL/api/sabores/?search=chocolate"
```

## 3. Productos

### Listar productos

```bash
curl $BASE_URL/api/productos/
```

### Crear producto

```bash
curl -X POST $BASE_URL/api/productos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "sabor": 1,
    "nombre": "Chocolate Premium",
    "codigo": "CH001",
    "precio_venta": 3.50,
    "costo_insumos": 1.20,
    "disponible": true
  }'
```

### Filtrar por sabor

```bash
curl "$BASE_URL/api/productos/?sabor=1"
```

### Filtrar por disponibilidad

```bash
curl "$BASE_URL/api/productos/?disponible=true"
```

### Buscar por nombre

```bash
curl "$BASE_URL/api/productos/?search=chocolate"
```

### Buscar por código

```bash
curl "$BASE_URL/api/productos/?search=CH001"
```

### Ordenar por precio

```bash
curl "$BASE_URL/api/productos/?ordering=precio_venta"
```

### Obtener producto específico

```bash
curl $BASE_URL/api/productos/1/
```

### Actualizar producto

```bash
curl -X PUT $BASE_URL/api/productos/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "sabor": 1,
    "nombre": "Chocolate Oscuro Premium",
    "codigo": "CH001",
    "precio_venta": 4.50,
    "costo_insumos": 1.50,
    "disponible": true
  }'
```

### Eliminar producto

```bash
curl -X DELETE $BASE_URL/api/productos/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## 4. Pedidos (Descuento por Volumen)

### Pedido sin descuento (1-3 unidades)

```bash
curl -X POST $BASE_URL/api/pedido/ \
  -H "Content-Type: application/json" \
  -d '[
    {
      "nombre": "Chocolate",
      "precio": 3.50,
      "cantidad": 2
    }
  ]'
```

**Respuesta:**
```json
{
  "total_unidades": 2,
  "subtotal": 7.00,
  "descuento_pct": 0,
  "total": 7.00,
  "detalle": [
    {
      "nombre": "Chocolate",
      "cantidad": 2,
      "subtotal_linea": 7.00
    }
  ]
}
```

### Pedido con descuento 10% (4-6 unidades)

```bash
curl -X POST $BASE_URL/api/pedido/ \
  -H "Content-Type: application/json" \
  -d '[
    {
      "nombre": "Chocolate",
      "precio": 3.50,
      "cantidad": 2
    },
    {
      "nombre": "Fresa",
      "precio": 3.00,
      "cantidad": 3
    }
  ]'
```

### Pedido con descuento 15% (7-10 unidades)

```bash
curl -X POST $BASE_URL/api/pedido/ \
  -H "Content-Type: application/json" \
  -d '[
    {
      "nombre": "Chocolate",
      "precio": 3.50,
      "cantidad": 3
    },
    {
      "nombre": "Fresa",
      "precio": 3.00,
      "cantidad": 4
    },
    {
      "nombre": "Vainilla",
      "precio": 2.50,
      "cantidad": 1
    }
  ]'
```

### Pedido con descuento 20% (más de 10 unidades)

```bash
curl -X POST $BASE_URL/api/pedido/ \
  -H "Content-Type: application/json" \
  -d '[
    {
      "nombre": "Chocolate",
      "precio": 3.50,
      "cantidad": 4
    },
    {
      "nombre": "Fresa",
      "precio": 3.00,
      "cantidad": 4
    },
    {
      "nombre": "Vainilla",
      "precio": 2.50,
      "cantidad": 3
    }
  ]'
```

**Respuesta:**
```json
{
  "total_unidades": 11,
  "subtotal": 33.50,
  "descuento_pct": 20,
  "total": 26.80,
  "detalle": [
    {
      "nombre": "Chocolate",
      "cantidad": 4,
      "subtotal_linea": 14.00
    },
    {
      "nombre": "Fresa",
      "cantidad": 4,
      "subtotal_linea": 12.00
    },
    {
      "nombre": "Vainilla",
      "cantidad": 3,
      "subtotal_linea": 7.50
    }
  ]
}
```

## 5. Producción (Planificación con WHILE)

### Calcular producción con presupuesto de 20

```bash
curl "$BASE_URL/api/produccion/?presupuesto=20&costos=4.5,3.0,6.0,5.5,4.0"
```

**Respuesta:**
```json
{
  "productos_producidos": 4,
  "presupuesto_gastado": 19.00,
  "presupuesto_restante": 1.00,
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
    },
    {
      "producto_numero": 4,
      "costo": 5.50
    }
  ]
}
```

### Calcular producción con presupuesto de 50

```bash
curl "$BASE_URL/api/produccion/?presupuesto=50&costos=10.0,8.5,7.0,9.5,6.0,5.5"
```

### Calcular producción con presupuesto bajo

```bash
curl "$BASE_URL/api/produccion/?presupuesto=10&costos=5.5,4.0,3.5,6.0"
```

## 6. Panel de Administración

Acceder a http://localhost:8000/admin/ con usuario `admin` y contraseña `admin123`

## Códigos de Error Comunes

- **401 Unauthorized**: Token expirado o no válido
- **403 Forbidden**: No tienes permisos (debes ser staff)
- **404 Not Found**: Recurso no encontrado
- **400 Bad Request**: Datos inválidos en la petición
