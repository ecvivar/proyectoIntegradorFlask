# Proyecto Integrador - Tienda Online Flask

Tienda online (e-commerce) desarrollada en Python con Flask y MySQL para la venta de remeras con diseños de bandas de música icónicas.

## Características

- Catálogo de productos con imágenes
- Sistema de usuarios (registro, login, logout)
- Carrito de compras (agregar, visualizar, eliminar productos)
- Integración con Mercado Pago para pagos electrónicos
- Panel de administración (ABM) para gestionar productos
- Búsqueda de productos por descripción

## Tecnologías

- **Backend:** Python, Flask, Flask-MySQL
- **Base de datos:** MySQL
- **Frontend:** HTML, CSS, Jinja2 templates
- **Pagos:** Mercado Pago SDK

## Requisitos

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv env
   ```
3. Activar entorno virtual:
   - Windows: `env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configurar MySQL:
   - Crear base de datos `final`
   - Importar `final.sql`
   - Actualizar credenciales en `app.py` si es necesario

## Ejecución

```bash
python app.py
```

Acceder a: `http://127.0.0.1:5000/`

## Usuarios

- **Usuario administrador:** con acceso completo al panel ABM.
- **Usuarios regulares:** pueden registrarse desde la web.

## Estructura del Proyecto

```
proyecto-integrador-final/
├── app.py                 # Aplicación principal
├── templates/             # Plantillas HTML
│   ├── productos.html
│   ├── login.html
│   ├── register.html
│   ├── carrito.html
│   ├── comprar.html
│   └── ...
├── static/                # Archivos estáticos
│   ├── css/
│   └── imagenes/
├── final.sql              # Base de datos
└── requirements.txt      # Dependencias
```