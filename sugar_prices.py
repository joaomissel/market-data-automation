import requests
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

headers = {
    "User-Agent": "Mozilla/5.0"
}

agora_ny = datetime.now(ZoneInfo("America/New_York"))

print(
    "Horário de New York:",
    agora_ny.strftime("%Y-%m-%d %H:%M:%S %Z")
)


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
