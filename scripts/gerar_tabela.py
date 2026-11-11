from itertools import product

print('Gerador de Tabela-Verdade')
print('-' * 40)

expressao = input('Digite a expressão (use "and", "or", "not"): ')
expressao = expressao.replace('(', ' ( ').replace(')', ' ) ')
expressao_dividida = expressao.lower().strip().split()

operadores = {'and', 'or', 'not', '(', ')'}
variaveis = []
for item in expressao_dividida:
    if item not in operadores and item not in variaveis:
        variaveis.append(item)

qnt_variaveis = len(variaveis)
variaveis.sort()
print(f'\nVariáveis encontradas: {variaveis}')
print(f'Expressão: {expressao}')
print(f'\n{" | ".join(variaveis)} | S')
print('-' * (qnt_variaveis * 4 + 4))

for combinacao in product([0, 1], repeat=qnt_variaveis):
    ambiente = dict(zip(variaveis, combinacao))
    resultado = eval(' '.join(expressao_dividida), {}, ambiente)
    resultado_inteiro = int(bool(resultado))
    linha = ' | '.join(str(v) for v in combinacao)
    print(f'{linha} | {resultado_inteiro}')