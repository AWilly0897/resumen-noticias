# Resumen Noticias

Este proyecto consulta titulares de política y economía de la semana pasada usando **NewsAPI**  
y los muestra en una página web sencilla desplegada en **Render**.

## Características

- Desarrollado con **Flask** y **Gunicorn**.
- Consume la API de **NewsAPI** (requiere clave `NEWSAPI_KEY`).
- Renderiza cada artículo con:
  - Título
  - Fecha y fuente
  - Descripción
  - Desarrollo del cuerpo
  - Separador visual estilo diario digital
- Incluye menú de navegación y favicon.

##  Estructura del proyecto


resumen-noticias-1/ │ ├── app.py              # Aplicación Flask ├── requirements.txt    # Dependencias necesarias ├── static/ │   └── Favicon.ico     # Ícono del sitio └── README.md           # Documentación del proyecto

##  Instalación local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/AWilly0897/resumen-noticias-1.git
   cd resumen-noticias-1


- Instalar dependencias:
pip install -r requirements.txt
- Definir la variable de entorno con tu clave de NewsAPI:
export NEWSAPI_KEY="tu_clave_aqui"


- Ejecutar la aplicación:
python app.py


La aplicación estará disponible en http://localhost:5000.
Despliegue en Render
- Crear un nuevo servicio web en Render.
- Conectar el repositorio de GitHub.
- Configurar:
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Definir la variable de entorno NEWSAPI_KEY en el panel de Render.
- Deploy y listo 🎉.
Vista previa
Cada artículo se muestra como un bloque con título, metadatos, descripción y cuerpo, separado por una línea divisoria, simulando el estilo de un diario digital.

---





