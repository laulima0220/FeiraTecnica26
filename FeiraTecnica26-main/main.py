from pymongo import MongoClient
from pymongo.server_api import ServerApi

from ZonaNorte import zona_norte
from ZonaSul import zona_sul
from ZonaLeste import zona_leste
from ZonaSudeste import zona_sudeste
from ZonaOeste import zona_oeste
from ZonaCentral import zona_central 

import webbrowser

# MAIN.PY COM O BANCO ATUALIZADOOOOOOO !! 
    #-> pra testar o mapa, vai ser preciso criar os botoes de cada zona no site, entao ainda nao foram testadas as formas que vão aparecer os pontos
    

# Conexão com o MongoDB Atlas

MONGO_URI = "mongodb+srv://root:123@cluster0.90z34ef.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1")
)

try:
    client.admin.command("ping")

    print("Conexao estabelecida com sucesso com o MongoDB Atlas!")

    banco = client["FeiraTecnica"]
    colecao = banco["passeios"]

except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit()

zonas = (
    zona_norte
    + zona_sul
    + zona_leste
    + zona_sudeste
    + zona_oeste
    + zona_central
)

#deixar comentado pra nao bugar 
    #colecao.delete_many({})
    #colecao.insert_many(zonas)


colecao.create_index([
    ("local", "2dsphere")
])
print("------------------ PONTOS PRÓXIMOS --------------------")


#while True:

    # Entrada da latitude

  #  while True:
       # try:
           # latitude = float(input("Insira a latitude: "))
          #  break

      #  except ValueError:
         #   print("Digite apenas um número válido.")

   # while True:
        #try:
           # longitude = float(input("Insira a longitude: "))
          #  break

     #   except ValueError:
         #   print("Digite apenas um número válido.")

  #  while True:
       # try:
          #  distancia = int(input("Insira a distância máxima em km: "))
          #  break

     #   except ValueError:
           # print("Digite apenas um número inteiro.")

   # distancia = distancia * 1000

    #consulta = {
       # "local": {
          #  "$near": {
              #  "$geometry": {
                #    "type": "Point",
                   # "coordinates": [longitude, latitude]
             #   },
               # "$maxDistance": distancia
           # }
       # }
   # }


   # resultado = colecao.find(consulta)
   # eventos_encontrados = list(resultado)

    #with open("mapa.html", "r", encoding="utf-8") as arquivo:
            #html = arquivo.read()

   # marcadores = ""

   # for evento in eventos_encontrados:

       # nome = evento["nome"]
       # local = evento["local"]["nome"]
      #  descricao = evento["descricao"]
       # categoria = evento["categoria"]

       # lon = evento["local"]["coordinates"][0]
       # lat = evento["local"]["coordinates"][1]

       # marcadores += f"""
       # L.marker([{lat}, {lon}])
           # .addTo(mapa)
           # .bindPopup(
             #   "<b>{nome}</b><br>" +
             #   "📍 {local}<br>" +
              #  "📂 {categoria}<br>" +
             #   "📃 {descricao}"
           # );
       # """

   # html = html.replace("{{MENSAGEM}}", mensagem)
   # html = html.replace("LATITUDE_AQUI", str(latitude))
   # html = html.replace("LONGITUDE_AQUI", str(longitude))
   # html = html.replace("// MARCADORES_AQUI", marcadores)

   # with open("mapa_gerado.html", "w", encoding="utf-8") as arquivo:
       # arquivo.write(html)

      #  webbrowser.open("mapa_gerado.html")