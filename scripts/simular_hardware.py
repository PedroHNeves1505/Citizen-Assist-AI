import json
import time
import random
import os

ARQUIVO = "data/fila_virtual.json"

def gerar_dados():
    pessoas = random.randint(3, 15)
    temperatura = random.uniform(22.0, 32.0)
    luminosidade = random.randint(50, 800)
    vibracao = random.uniform(0.01, 0.4)
    
    dados = {
        "pessoas": pessoas,
        "tempo_espera": round(pessoas * 2.5, 1),
        "temperatura": round(temperatura, 1),
        "luminosidade": luminosidade,
        "vibracao": round(vibracao, 2),
        "timestamp": time.strftime('%H:%M:%S')
    }
    
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)
    print(f"[{dados['timestamp']}] Hardware atualizado: {pessoas} pessoas | {temperatura}°C")

if __name__ == "__main__":
    print("Iniciando simulador de hardware ESP32 (Ctrl+C para parar)...")
    while True:
        gerar_dados()
        time.sleep(2)