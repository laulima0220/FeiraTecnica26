from pymongo import MongoClient
from pymongo.server_api import ServerApi
from eventos import evento
import webbrowser

# MAIN.PY antigo, tava sendo mantido pra teste ou coisas do tipo relacionados com o mapa!!!!!!

# Conexão com o MongoDB Atlas

MONGO_URI = "mongodb+srv://root:123@cluster0.90z34ef.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1")
)

try:
    client.admin.command("ping")

    print("Conexao estabelecida com sucesso com o MongoDB Atlas!")

    banco = client["projetos_python"]
    colecao = banco["eventos"]

except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit()

colecao.create_index([
    ("local", "2dsphere")
])


print("------------------ EVENTOS PRÓXIMOS --------------------")


while True:

    # Entrada da latitude

    while True:
        try:
            latitude = float(input("Insira a latitude: "))
            break

        except ValueError:
            print("Digite apenas um número válido.")

    while True:
        try:
            longitude = float(input("Insira a longitude: "))
            break

        except ValueError:
            print("Digite apenas um número válido.")

    while True:
        try:
            distancia = int(input("Insira a distância máxima em km: "))
            break

        except ValueError:
            print("Digite apenas um número inteiro.")

    distancia = distancia * 1000

    consulta = {
        "local": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": distancia
            }
        }
    }


    resultado = colecao.find(consulta)

    eventos_encontrados = list(resultado)

    if not eventos_encontrados:
        print("---- Nenhum evento encontrado nessa distância... :(")

        mensagem = "Nenhum evento encontrado nessa distância... :("

    else:
        mensagem = f"{len(eventos_encontrados)} evento(s) encontrado(s)!"

    with open("mapa.html", "r", encoding="utf-8") as arquivo:
            html = arquivo.read()

    marcadores = ""

    for evento in eventos_encontrados:

        nome = evento["nome"]
        local = evento["local"]["nome"]
        descricao = evento["descricao"]
        categoria = evento["categoria"]

        lon = evento["local"]["coordinates"][0]
        lat = evento["local"]["coordinates"][1]

        marcadores += f"""
        L.marker([{lat}, {lon}])
            .addTo(mapa)
            .bindPopup(
                "<b>{nome}</b><br>" +
                "📍 {local}<br>" +
                "📂 {categoria}<br>" +
                "📃 {descricao}"
            );
        """

    html = html.replace("{{MENSAGEM}}", mensagem)
    html = html.replace("LATITUDE_AQUI", str(latitude))
    html = html.replace("LONGITUDE_AQUI", str(longitude))
    html = html.replace("// MARCADORES_AQUI", marcadores)

    with open("mapa_gerado.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(html)

        webbrowser.open("mapa_gerado.html")

    novamente = input("\nDeseja fazer outra busca? (s/n): ")


    while novamente.lower() != "s" and novamente.lower() != "n":

        print("Digite apenas s ou n.")

        novamente = input("Deseja fazer outra busca? (s/n): ")


    if novamente.lower() != "s":

        print("\nPrograma encerrado!")

        break