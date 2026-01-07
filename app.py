from flask import Flask, request, redirect, url_for
import requests
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)

# --- Funciones auxiliares ---
def guardar_articulo(titulo, descripcion, cuerpo, fuente, fecha):
    os.makedirs("data", exist_ok=True)
    existentes = []
    if os.path.exists("data/index.json"):
        with open("data/index.json", encoding="utf-8") as f:
            existentes = [json.loads(line) for line in f]

    # Evitar duplicados por título
    if any(e["titulo"] == titulo for e in existentes):
        return

    entrada = {
        "titulo": titulo,
        "descripcion": descripcion,
        "cuerpo": cuerpo,
        "fuente": fuente,
        "fecha": fecha,
        "estado": "pendiente"
    }
    with open("data/index.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada) + "\n")

def comentario_ia(titulo):
    return {
        "nombre": "IA",
        "comentario": f"Este artículo analiza el tema: {titulo}, con implicancias políticas y económicas relevantes."
    }

def guardar_comentario(comentario):
    os.makedirs("data", exist_ok=True)
    with open("data/comentarios.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(comentario) + "\n")

# --- Menú de navegación fijo ---
def menu():
    return """
    <nav style="background-color:#eee;padding:10px;">
        <a href="/">Resumen</a> |
        <a href="/ver">Índice</a> |
        <a href="/publicar">Publicar</a>
    </nav>
    """

# --- Rutas principales ---
@app.route("/")
def resumen():
    hoy = datetime.utcnow()
    inicio = hoy - timedelta(days=7)
    fecha_inicio = inicio.strftime("%Y-%m-%d")

    api_key = os.environ.get("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q=politica+economia&from={fecha_inicio}&sortBy=publishedAt&apiKey={api_key}"
    resp = requests.get(url).json()

    # Leer artículos existentes para evitar duplicados
    existentes = []
    if os.path.exists("data/index.json"):
        with open("data/index.json", encoding="utf-8") as f:
            existentes = [json.loads(line) for line in f]

    titulares = []
    for art in resp.get("articles", [])[:10]:
        titulo = art["title"]
        if any(e["titulo"] == titulo for e in existentes):
            continue  # Saltar si ya existe

        descripcion = art.get("description", "Sin descripción")
        cuerpo = art.get("content", "Sin cuerpo disponible")
        fuente = art["source"]["name"]
        fecha = art["publishedAt"]

        guardar_articulo(titulo, descripcion, cuerpo, fuente, fecha)
        guardar_comentario(comentario_ia(titulo))
        titulares.append(titulo)

    # Generar HTML con Favicon y menú
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resumen semanal de política y economía</title>
        <link rel="icon" href="{url_for('static', filename='Favicon.ico')}" type="image/x-icon" />
    </head>
    <body>
        {menu()}
        <h1>Resumen semanal de política y economía</h1>
        <ul>
    """
    for t in titulares:
        html += f"<li>{t}</li>"
    html += """
        </ul>
    </body>
    </html>
    """
    return html

@app.route("/ver")
def ver_indice():
    try:
        with open("data/index.json", encoding="utf-8") as f:
            entradas = [json.loads(line) for line in f]
    except FileNotFoundError:
        entradas = []

    html = f"<h1>Índice editorial</h1>{menu()}<ul>"
    for e in entradas:
        html += f"<li>{e['fecha']} - {e['titulo']} - {e['estado']} "
        html += f"<a href='/aprobar?titulo={e['titulo']}'>[Aprobar]</a></li>"
    html += "</ul>"

    # Botón extra para desaprobar duplicados
    html += """
    <p>
        <a href='/desaprobar_duplicados'>
            <button style="background-color:red;color:white;padding:8px;border:none;border-radius:4px;">
                Desaprobar duplicados
            </button>
        </a>
    </p>
    """
    return html

@app.route("/aprobar")
def aprobar():
    titulo = request.args.get("titulo")
    nuevas = []
    try:
        with open("data/index.json", encoding="utf-8") as f:
            for line in f:
                entrada = json.loads(line)
                if entrada["titulo"] == titulo:
                    entrada["estado"] = "aprobado"
                nuevas.append(entrada)
        # Reescribir el archivo con los cambios
        with open("data/index.json", "w", encoding="utf-8") as f:
            for e in nuevas:
                f.write(json.dumps(e) + "\n")
    except FileNotFoundError:
        return "No hay artículos cargados todavía."

    return redirect("/ver")

@app.route("/desaprobar_duplicados")
def desaprobar_duplicados():
    nuevas = []
    vistos = set()
    try:
        with open("data/index.json", encoding="utf-8") as f:
            for line in f:
                entrada = json.loads(line)
                titulo = entrada["titulo"]
                if titulo in vistos:
                    entrada["estado"] = "desaprobado"
                else:
                    vistos.add(titulo)
                nuevas.append(entrada)

        # Reescribir el archivo con los cambios
        with open("data/index.json", "w", encoding="utf-8") as f:
            for e in nuevas:
                f.write(json.dumps(e) + "\n")

    except FileNotFoundError:
        return "No hay artículos cargados todavía."

    return redirect("/ver")

@app.route("/publicar")
def publicar():
    try:
        with open("data/index.json", encoding="utf-8") as f:
            entradas = [json.loads(line) for line in f]
    except FileNotFoundError:
        return "No hay artículos cargados todavía."

    # Verificar si todos están aprobados
    if all(e["estado"] == "aprobado" for e in entradas):
        html = f"<h1>Artículos publicados</h1>{menu()}<ul>"
        for e in entradas:
            html += f"<li>{e['fecha']} - {e['titulo']} - {e['descripcion']}</li>"
        html += "</ul>"
        return html
    else:
        html = f"<h1>No todos los artículos están aprobados</h1>{menu()}<ul>"
        for e in entradas:
            html += f"<li>{e['fecha']} - {e['titulo']} - {e['estado']}</li>"
        html += "</ul>"
        return html

# --- Ejecución ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

