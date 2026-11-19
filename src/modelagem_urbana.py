import numpy as np

REGIOES = ['Norte', 'Sul', 'Leste', 'Oeste']

A = np.array([
    [1, 1, 1, 1],
    [1, 2, 0, 1],
    [0, 1, 2, 0],
    [1, 0, 1, 2]
], dtype=float)

b = np.array([72, 76, 52, 76], dtype=float)

PASSAGEIROS = np.array([560, 760, 720, 840])
CAPACIDADE_ONIBUS = 40


def distribuição_atual():
    """Resolve o sistema linear e retorna a distribuição atual (arredondada)."""
    x = np.linalg.solve(A, b)
    return np.round(x).astype(int)


def demanda_necessaria():
    """Retorna quantos ônibus cada região precisa para atender a demanda."""
    return (PASSAGEIROS / CAPACIDADE_ONIBUS).astype(int)


def redistribuir():
    """Aplica a transformação linear e retorna a nova distribuição."""
    M = np.array([
        [1.0,  1/20, 0.0,  1/24],
        [0.0, 19/20, 0.0,  0.00],
        [0.0,  0.00, 1.0,  2/24],
        [0.0,  0.00, 0.0, 21/24]
    ])
    return np.round(M @ distribuição_atual()).astype(int)


def exibir_distribuicao():
    """Exibe a comparação entre frota atual, demanda e redistribuída."""
    atual = distribuição_atual()
    necessaria = demanda_necessaria()
    nova = redistribuir()

    print("\n" + "=" * 65)
    print("   DISTRIBUIÇÃO DA FROTA DE ÔNIBUS — MOBILIDADE URBANA")
    print("=" * 65)
    print(f"{'Região':<10}{'Frota Atual':>13}{'Demanda':>10}{'Redistribuída':>15}{'Saldo':>8}")
    print("-" * 65)

    for i, regiao in enumerate(REGIOES):
        saldo = nova[i] - necessaria[i]
        print(f"{regiao:<10}{atual[i]:>13}{necessaria[i]:>10}{nova[i]:>15}{saldo:>+8}")

    print("-" * 65)
    print(f"{'TOTAL':<10}{atual.sum():>13}{necessaria.sum():>10}{nova.sum():>15}")
    print("\nApós a redistribuição, 100% da demanda é atendida sem")
    print("   ampliar a frota total de 72 ônibus.")
    print("\nO que isso significa para você?")
    print("   - Norte e Leste recebem mais ônibus (menos superlotação).")
    print("   - Sul e Oeste transferem veículos ociosos para as regiões")
    print("     que precisam.")
    print("=" * 65)


def consultar_regiao(nome_regiao: str):
    """Mostra apenas os dados de uma região específica."""
    nome_regiao = nome_regiao.strip().capitalize()
    if nome_regiao not in REGIOES:
        print(f"\nRegião '{nome_regiao}' não encontrada. Opções: {', '.join(REGIOES)}")
        return

    i = REGIOES.index(nome_regiao)
    atual = distribuição_atual()
    necessaria = demanda_necessaria()
    nova = redistribuir()

    print(f"\n--- REGIÃO {nome_regiao.upper()} ---")
    print(f"Frota atual:        {atual[i]} ônibus")
    print(f"Demanda no pico:    {necessaria[i]} ônibus")
    print(f"Após redistribuição: {nova[i]} ônibus")

    if nova[i] >= necessaria[i]:
        print("Após a redistribuição, a demanda é totalmente atendida!")
    else:
        print("Ainda há déficit mesmo após a redistribuição.")