from flask import Flask, render_template, abort
from pymongo import MongoClient
from pymongo.server_api import ServerApi

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

app.run(debug=True)