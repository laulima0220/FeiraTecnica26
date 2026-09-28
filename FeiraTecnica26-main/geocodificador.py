import requests

# Nominatim: serviço gratuito de geocodificação do OpenStreetMap
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def buscar_coordenadas(endereco):
    """
    Recebe um texto de endereço (ex: "Rua Siqueira Campos")
    e devolve (latitude, longitude) ou None se não encontrar nada.
    """

    # Sempre completa a busca com cidade e país fixos,
    # assim o usuário não precisa digitar isso toda vez
    # e evita confundir com outras ruas com mesmo nome de outra cidade.
    endereco_completo = f"{endereco}, São José dos Campos, Brasil"

    parametros = {
        "q": endereco_completo,
        "format": "json",
        "limit": 1
    }

    # O Nominatim exige um identificador no cabeçalho da requisição
    cabecalhos = {
        "User-Agent": "FeiraTecnica26-App"
    }

    resposta = requests.get(NOMINATIM_URL, params=parametros, headers=cabecalhos)

    dados = resposta.json()

    if not dados:
        return None

    resultado = dados[0]

    latitude = float(resultado["lat"])
    longitude = float(resultado["lon"])

    return (latitude, longitude)


# Bloco de teste: roda quando executamos este arquivo diretamente
if __name__ == "__main__":

    enderecos_teste = [
        "Rua Siqueira Campos",
        "Avenida Cassiano Ricardo",
        "Rua Que Não Existe De Jeito Nenhum 99999"
    ]

    for endereco in enderecos_teste:
        print(f"Buscando: {endereco}")

        coordenadas = buscar_coordenadas(endereco)

        if coordenadas is None:
            print("  -> Nenhum resultado encontrado.\n")
        else:
            lat, lon = coordenadas
            print(f"  -> Latitude: {lat} | Longitude: {lon}\n")