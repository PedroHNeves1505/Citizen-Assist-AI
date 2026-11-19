import json
import os

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_FILA = os.path.join(PASTA_PROJETO, "data", "fila_virtual.json")

def ler_dados_fila():
    """Lê os dados da fila virtual (simulados pelo Wokwi)."""
    try:
        with open(ARQUIVO_FILA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def exibir_status_fila():
    dados = ler_dados_fila()
    if not dados:
        print("\nALERTA: Não foi possível ler os dados da fila virtual.")
        print("Verifique se o arquivo data/fila_virtual.json existe.")
        return

    print("\n" + "=" * 50)
    print("FILA VIRTUAL — STATUS ATUAL")
    print("=" * 50)
    print(f"Pessoas na fila: {dados['pessoas']}")
    print(f"Tempo estimado de espera: {dados['tempo_espera']:.1f} minutos")
    print(f"Temperatura na sala: {dados['temperatura']:.1f} °C")
    print(f"Luminosidade: {dados['luminosidade']} Lux")
    print(f"Vibração: {dados['vibracao']:.2f} g")

    print("\n--- ALERTAS ---")
    alertas = []
    if dados['temperatura'] > 30:
        alertas.append("Temperatura alta (>30°C). Beba água e procure um lugar fresco.")
    if dados['luminosidade'] < 100:
        alertas.append("Ambiente com pouca luz. Cuidado com quedas.")
    if dados['vibracao'] > 0.5:
        alertas.append("Vibração detectada. Verifique se houve alguma queda.")
    if dados['pessoas'] > 20:
        alertas.append("Fila muito longa (>20 pessoas). Considere voltar mais tarde.")

    if alertas:
        for alerta in alertas:
            print(f" - {alerta}")
    else:
        print(" - Nenhum alerta. Ambiente normal.")
    print("=" * 50)