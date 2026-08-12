import requests
import json
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0"
}


def obter_previous(contrato):
    url = f"https://www.barchart.com/futures/quotes/{contrato}"

    r = requests.get(url, headers=headers)

    inicio = r.text.find(f'{{"{contrato}"')
    fim = r.text.find("</script>", inicio)

    if inicio == -1 or fim == -1:
        return None

    try:
        texto_json = r.text[inicio:fim].strip()
        dados = json.loads(texto_json)

        return dados[contrato]["quote"]

    except:
        return None


contratos = [
    "SBV26",
    "SBH27",
    "SBK27",
    "SBN27",
    "SBV27"
]


resultado = []

for contrato in contratos:

    dados = obter_previous(contrato)

    if dados is not None:

        resultado.append({
            "Contrato": contrato,
            **dados
        })


df = pd.DataFrame(resultado)

print(df)
