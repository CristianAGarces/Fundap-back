# fundapmacoe-backend

Este es el backend del proyecto FundapMacoe. Proporciona una API para la gestión de administradores e interesadas, autenticación y servicios relacionados.

## Estructura del proyecto

- `main.py`: Punto de entrada principal de la API.
- `endpoinds/`: Rutas de la API para administradores e interesadas.
- `funciones/`: Funciones auxiliares para lógica de negocio, autenticación y utilidades de correo.
- `middlewares/`: Middleware para autenticación JWT.
- `Schemas/`: Esquemas de datos para validación y serialización.
- `services/`: Servicios externos, como integración con Supabase.
- `venv311/`: Entorno virtual de Python.

## Requisitos

- Python 3.11 o superior
- Instalar dependencias con:

```pwsh
pip install -r venv311/requirements.txt
```

## Ejecución

```pwsh
python main.py
```

## Notas

- Asegúrate de tener configuradas las variables de entorno necesarias para la conexión a servicios externos.
- Para desarrollo, puedes usar herramientas como Postman para probar los endpoints.
