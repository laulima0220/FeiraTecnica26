from flask import Flask, render_template, abort, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from geocodificador import buscar_coordenadas

app = Flask(__name__)

# Conexão com o MongoDB (a mesma do main.py)
MONGO_URI = "mongodb+srv://root:123@cluster0.90z34ef.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
colecao = client["FeiraTecnica"]["passeios"]

# chave (usada na URL) -> nome bonito (mostrado no botão)
ZONAS = {
    "norte": "Zona Norte",
    "sul": "Zona Sul",
    "leste": "Zona Leste",
    "sudeste": "Zona Sudeste",
    "oeste": "Zona Oeste",
    "central": "Centro",
}

@app.route("/")
def home():
    return render_template("index.html", zonas=ZONAS)

@app.route("/mapa/<zona>")
def mapa(zona):
    if zona not in ZONAS:
        abort(404)

    passeios = list(colecao.find({"zona": zona}, {"_id": 0}))

    return render_template("mapa.html", titulo=ZONAS[zona], passeios=passeios)

@app.route("/mapa/perto")
def mapa_perto():
    # Lê o que veio do formulário (name="endereco" e name="distancia")
    endereco = request.args.get("endereco")
    distancia = request.args.get("distancia", type=int)

    if not endereco or not distancia:
        abort(400)

    # Transforma o endereço digitado em coordenadas
    coordenadas = buscar_coordenadas(endereco)

    if coordenadas is None:
        # Endereço não encontrado: mostra o mapa vazio, sem quebrar a página
        return render_template(
            "mapa.html",
            titulo=f"Endereço não encontrado: {endereco}",
            passeios=[]
        )

    latitude, longitude = coordenadas
    distancia_em_metros = distancia * 1000

    # Mesma lógica de consulta $near que já existia no main.py antigo
    consulta = {
        "local": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": distancia_em_metros
            }
        }
    }

    passeios = list(colecao.find(consulta, {"_id": 0}))

    titulo = f"Perto de: {endereco}"

    return render_template("mapa.html", titulo=titulo, passeios=passeios)

app.run(debug=True)