from flask import Flask, url_for
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def menu():
    return """
    <nav style="background-color:#eee;padding:10px;">
        <a href="/">Resumen</a>
    </nav>
    """

@app.route("/")
def resumen():
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    api_key = os.environ.get("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey={api_key}"
    resp = requests.get(url).json()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resumen semanal</title>
        <link rel="icon" href="{url_for('static', filename='Favicon.ico')}" type="image/x-icon" />
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
            h2 {{
                color: #2c3e50;
                margin-top: 20px;
            }}
            .articulo {{
                background: #fff;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .meta {{
                font-size: 0.9em;
                color: #777;
                margin-bottom: 10px;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        {menu()}
        <h1>Resumen semanal de política y economía</h1>
    """

    for art in resp.get("articles", [])[:10]:
        titulo = art.get("title", "Sin título")
        descripcion = art.get("description", "Sin descripción disponible")
        cuerpo = art.get("content", "Sin cuerpo disponible")
        fuente = art["source"]["name"]
        fecha = art["publishedAt"]

        html += f"""
        <div class="articulo">
            <h2>{titulo}</h2>
            <p class="meta"><strong>Fecha:</strong> {fecha} | <strong>Fuente:</strong> {fuente}</p>
            <p><em>{descripcion}</em></p>
            <p>{cuerpo}</p>
        </div>
        <hr>
        """

    html += "</body></html>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

