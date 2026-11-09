from src.base_conhecimento import BaseConhecimento
from src.assistente import Assistente

def main():
    print("=" * 50)
    print("INICIALIZANDO O CITIZEN ASSIST AI")
    print("=" * 50)

    caminho_csv = 'data/base_conhecimento.csv'

    base = BaseConhecimento(caminho_csv)
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    try:
        assistente.menu()
    except SystemExit:
        pass

    print("\n" + "=" * 50)
    print("RELATÓRIO DE INDICADORES FINAIS")
    print("=" * 50)
    
    relatorio = assistente.indicadores()

    if isinstance(relatorio, list):
        porcentagem_ajudou, porcentagem_encontrou, tempo_medio, tentativas, facilidade, sem_solucao = relatorio
        
        print(f"Taxa de respostas encontradas: {porcentagem_encontrou:.2f}%")
        print(f"Taxa de respostas que ajudaram: {porcentagem_ajudou:.2f}%")
        print(f"Tempo médio de busca: {tempo_medio:.2f} segundos")
        print(f"Média de tentativas por atendimento: {tentativas:.2f}")
        print(f"Facilidade de uso (1 a 5): {facilidade:.2f}")
        
        print("\nDúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f" - {duvida}")
        else:
            print(" - Nenhuma dúvida ficou sem solução!")
    else:
        print(relatorio)
        
    print("=" * 50)

if __name__ == "__main__":
    main()