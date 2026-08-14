import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# DATA ATUAL - SÃO PAULO
# =========================

agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

data = agora.strftime("%Y-%m-%d")

print(
    "Data de São Paulo:",
    agora.strftime("%Y-%m-%d %H:%M:%S %Z")
)


# =========================
# API PTAX - BANCO CENTRAL
# =========================

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    f"CotacaoDolarDia(dataCotacao=@dataCotacao)?"
    f"@dataCotacao='{agora.strftime('%m-%d-%Y')}'"
    "&$format=json"
)


# =========================
# CONSULTA
# =========================

response = requests.get(
    url,
    timeout=15
)

print("Status API:", response.status_code)


# =========================
# DADOS
# =========================

dados = response.json()

cotacoes = dados["value"]


if len(cotacoes) == 0:

    print("Nenhuma cotação encontrada para a data.")

else:

    cotacao = cotacoes[0]

    resultado = [{
        "Data": data,
        "PTAX Compra": cotacao["cotacaoCompra"],
        "PTAX Venda": cotacao["cotacaoVenda"],
        "Data/Hora Cotação": cotacao["dataHoraCotacao"]
    }]

    df = pd.DataFrame(resultado)


    # =========================
    # RESULTADO
    # =========================

    print("\n==============================")
    print("PTAX")
    print("==============================\n")

    print(df.to_string(index=False))


    # =========================
    # HISTÓRICO
    # =========================

    arquivo_historico = "ptax_history.csv"

    try:

        historico = pd.read_csv(
            arquivo_historico
        )

        historico = pd.concat(
            [historico, df],
            ignore_index=True
        )

    except (
        FileNotFoundError,
        pd.errors.EmptyDataError
    ):

        historico = df.copy()


    # =========================
    # REMOVER DUPLICIDADES
    # =========================

    historico = historico.drop_duplicates(
        subset=["Data"],
        keep="last"
    )


    # =========================
    # ORDENAR HISTÓRICO
    # =========================

    historico = historico.sort_values(
        by=["Data"]
    )


    # =========================
    # SALVAR HISTÓRICO
    # =========================

    historico.to_csv(
        arquivo_historico,
        index=False
    )

    print(
        "\nHistórico PTAX atualizado com sucesso."
    )


    # =========================
    # EXPORTAR COTAÇÃO ATUAL
    # =========================

    df.to_csv(
        "ptax.csv",
        index=False
    )

    print(
        "\nArquivo ptax.csv criado com sucesso."
    )


    # =========================
    # FINAL
    # =========================

    print("\n==============================")
    print("Processo concluído.")
    print("==============================")
