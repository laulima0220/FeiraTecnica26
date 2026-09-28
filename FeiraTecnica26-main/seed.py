from pymongo import MongoClient
from pymongo.server_api import ServerApi

from ZonaNorte import zona_norte
from ZonaSul import zona_sul
from ZonaLeste import zona_leste
from ZonaSudeste import zona_sudeste
from ZonaOeste import zona_oeste
from ZonaCentral import zona_central

MONGO_URI = "mongodb+srv://root:123@cluster0.90z34ef.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
colecao = client["FeiraTecnica"]["passeios"]

# Cada lista recebe o "nome" da sua zona
zonas = {
    "norte": zona_norte,
    "sul": zona_sul,
    "leste": zona_leste,
    "sudeste": zona_sudeste,
    "oeste": zona_oeste,
    "central": zona_central,
}

documentos = []

for nome_zona, lista in zonas.items():
    for ponto in lista:
        ponto["zona"] = nome_zona    # adiciona o campo novo
        documentos.append(ponto)

colecao.delete_many({})              # apaga os antigos para não duplicar
colecao.insert_many(documentos)
colecao.create_index([("local", "2dsphere")])

print(f"{len(documentos)} pontos inseridos!")