from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route("/")
def resumen():
    # Calcular semana pasada
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    # Obtener la API Key desde variable de entorno
    api_key = os.environ.get("NEWSAPI_KEY")

    # Construir la URL con la clave
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey={api_key}"
    resp = requests.get(url).json()

    # Generar resumen simple
    titulares = [art["title"] for art in resp.get("articles", [])[:10]]

    # Renderizar en HTML básico
    html = "<h1>Resumen semanal de política y economía</h1><ul>"
    for t in titulares:
        html += f"<li>{t}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

