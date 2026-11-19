import re
from .utils import apagar_terminal, normalizar
import sys
import time
import csv
import os
from .modulo_decisao import ModuloDecisao
from .gerenciador_orientacoes import GerenciadorOrientacoes
from .auth import fazer_login
from .fila_virtual import exibir_status_fila
from .modelagem_urbana import exibir_distribuicao, consultar_regiao

class Assistente():
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.notas_sessao = []
        self.perguntas_sem_solucao_sessao = []
        self.gerenciador = GerenciadorOrientacoes()
        self.logado = False   

    def menu(self):
        while True:
            print(f'\n{"=" * 50}')
            print(f'   Bem Vindo ao {self.nome}')
            print(f'{"=" * 50}')
            print('1. Fazer uma pergunta (busca inteligente com confiança)')
            print('2. Navegar por categorias')
            print('3. Pesquisar orientação (escolher palavra-chave)')
            print('4. Ordenar orientações')
            print('5. Listar todas as orientações')
            print('6. Consultar fila virtual')
            print('7. Consultar consumo de energia')
            print('8. Consultar distribuição de ônibus')
            if self.logado:
                print('9. Cadastrar orientação')
                print('10. Consultar orientação por ID')
                print('11. Atualizar orientação')
                print('12. Excluir orientação')
                print('13. Logout')
                opcoes_validas = list(range(0, 11))
            else:
                print('9. Acesso restrito (login)')
                opcoes_validas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            print('\n0. Sair')
            print('-' * 50)

            try:
                escolha = int(input('Digite o valor da opção desejada: '))
            except ValueError:
                print('Atenção: opção inválida! Tente novamente.')
                apagar_terminal()
                continue

            if escolha not in opcoes_validas:
                print('Atenção: opção inválida! Tente novamente.')
                apagar_terminal()
                continue

            match escolha:
                case 0:
                    print('Saindo do sistema!')
                    try:
                        nota = int(input('\nComo você pontua a facilidade do programa? De 1 a 5: '))
                        if 1 <= nota <= 5:
                            self.notas_sessao.append(nota)
                            self.salvar_nota(nota)
                        else:
                            print('Nota fora da faixa (1 a 5). Registrando 0.')
                            self.notas_sessao.append(0)
                            self.salvar_nota(0)
                    except ValueError:
                        print('Valor inválido. Registrando 0.')
                        self.notas_sessao.append(0)
                        self.salvar_nota(0)
                    print('Obrigado pelo retorno!')
                    time.sleep(2)
                    sys.exit()
                case 1:
                    self.perguntar()
                case 2:
                    self.navegar()
                case 3:
                    self.gerenciador.pesquisar()
                    apagar_terminal()
                case 4:
                    self.gerenciador.ordenar()
                    apagar_terminal()
                case 5:
                    self.gerenciador.listar()
                    apagar_terminal()
                case 6: 
                    exibir_status_fila()
                    apagar_terminal()
                case 7:
                    self.gerenciador.consultar()
                    apagar_terminal()
                case 8:
                        print("\n1) Ver todas as regiões")
                        print("2) Consultar uma região específica")
                        sub = input("Escolha: ").strip()
                        if sub == '1':
                            exibir_distribuicao()
                        elif sub == '2':
                            regiao = input("Qual região? (Norte/Sul/Leste/Oeste): ")
                            consultar_regiao(regiao)
                        else:
                            print("Opção inválida.")
                        apagar_terminal()
                case 9:
                    if self.logado:
                        self.gerenciador.cadastrar()
                        self.base.carregar()
                        apagar_terminal()
                    else:
                        if fazer_login():
                            self.logado = True
                        time.sleep(1)
                        apagar_terminal()
                case 10:
                    self.gerenciador.atualizar()
                    self.base.carregar()
                    apagar_terminal()
                case 11:
                    self.gerenciador.excluir()
                    self.base.carregar()
                    apagar_terminal()
                case 12:
                    self.logado = False
                    time.sleep(1)
                    apagar_terminal()

    def perguntar(self):
        padrao_cpf_ou_telefone = r"(\b\d{3}[\.\s-]?\d{3}[\.\s-]?\d{3}[\.\s-]?\d{2}\b)|(\b(?:\+?55\s*)?(?:\(\d{2}\)|\d{2})[\s.-]?\d{4,5}[\s.-]?\d{4}\b)"
        while True:
            pergunta = input('Digite a sua dúvida: ').strip()
            if re.search(padrao_cpf_ou_telefone, pergunta) or '@' in pergunta:
                print('Atenção: não digite CPF, telefone ou e-mail. Reescreva.')
                apagar_terminal()
                continue
            else:
                break

        inicio = time.time()
        resultados = self.base.buscar(pergunta)
        tempo = round(time.time() - inicio, 1)

        if not resultados:
            print('Não encontrei. Tente navegar pelas categorias.')
            self.perguntas_sem_solucao_sessao.append(pergunta)
            self.registrar(pergunta, 'pergunta', 'N/A', 'nao', 'nao', 1, tempo)
            time.sleep(2)
            apagar_terminal()
            return

        pontos, orientacao = resultados[0]
        if pontos >= 6:
            print(f'Confiança ALTA ({pontos:.1f} pontos)')
        elif pontos >= 3:
            print(f'Confiança MÉDIA ({pontos:.1f} pontos)')
        else:
            print('Confiança BAIXA. Não encontrei uma resposta exata.')
            self.perguntas_sem_solucao_sessao.append(pergunta)
            self.registrar(pergunta, 'pergunta', 'N/A', 'nao', 'nao', 1, tempo)
            time.sleep(2)
            apagar_terminal()
            return

        orientacao.exibir()
        self.oferecer_verificacao_elegibilidade(orientacao)

        ajudou = input('Essa orientação respondeu sua dúvida? (s/n): ').lower()
        while ajudou not in ['s', 'n']:
            ajudou = input('Digite apenas s ou n: ').lower()
        apagar_terminal()

        self.registrar(
            pergunta=pergunta,
            origem='pergunta',
            id_orientacao=orientacao.id_orientacao,
            encontrou='sim',
            ajudou=ajudou,
            tentativa=1,
            tempo=tempo
        )

    def navegar(self):
        while True:
            cont = 1
            opcoes_possiveis = []
            print('-' * 40)
            print('CATEGORIAS')
            for categoria in self.base.categorias():
                print(f'{cont}. {categoria}')
                opcoes_possiveis.append(cont)
                cont += 1
            print('0. Voltar')
            print('-' * 40)
            try:
                id_categoria_escolhida = int(input('\nDigite a categoria desejada: '))
                if id_categoria_escolhida == 0:
                    print('Retornando ao menu.')
                    time.sleep(1)
                    apagar_terminal()
                    return
                elif id_categoria_escolhida not in opcoes_possiveis:
                    print('\nAviso: Digite um valor dentro da sequência!')
                    time.sleep(1)
                    apagar_terminal()
                    continue
                break
            except ValueError:
                print('\nAviso: Digite um valor dentro da sequência!')
                time.sleep(1)
                apagar_terminal()
                continue

        inicio = time.time()
        lista_categoria = self.base.categorias()
        categoria_escolhida = lista_categoria[id_categoria_escolhida - 1]
        lista = self.base.por_categoria(categoria_escolhida)

        while True:
            if not lista:
                print('Nenhuma orientação nesta categoria.')
                time.sleep(2)
                return
            else:
                cont = 0
                print('-' * 40)
                for item in lista:
                    cont += 1
                    print(f'{cont}. {item.titulo}')
                print('0. Voltar')
                print('-' * 40)
                opcao_escolhida = input('\nDigite a opção desejada: ')

            if opcao_escolhida == '0':
                print('Retornando.')
                time.sleep(1)
                apagar_terminal()
                return
            try:
                opcao = int(opcao_escolhida)
                if 1 <= opcao <= len(lista):
                    tempo = round(time.time() - inicio, 1)
                    apagar_terminal()
                    lista[opcao - 1].exibir()
                    self.oferecer_verificacao_elegibilidade(lista[opcao - 1])

                    ajudou = input('Essa orientação respondeu sua dúvida? (s/n): ').lower()
                    while ajudou not in ['s', 'n']:
                        ajudou = input('Digite apenas s ou n: ').lower()

                    self.registrar(
                        pergunta=f'Navegação por categoria: {categoria_escolhida} -> {lista[opcao - 1].titulo}',
                        origem='categoria',
                        id_orientacao=lista[opcao - 1].id_orientacao,
                        encontrou='sim',
                        ajudou=ajudou,
                        tentativa=1,
                        tempo=tempo
                    )
                    apagar_terminal()
                    inicio = time.time()
                else:
                    print('Opção inválida! Tente novamente.')
                    time.sleep(1)
                    apagar_terminal()
                    continue
            except ValueError:
                print(f'Valor indisponível. Tente um valor entre 0 e {cont}')
                time.sleep(1)
                apagar_terminal()
                continue

    def oferecer_verificacao_elegibilidade(self, orientacao):
        if not orientacao.expressao_booleana:
            return

        print()
        resposta = input('Deseja verificar se você tem direito a este benefício? (sim ou não): ').lower()
        resposta = normalizar(resposta).strip()
        while resposta not in ['sim', 'nao']:
            resposta = input('Digite apenas sim ou não: ').strip().lower()
            resposta = normalizar(resposta).strip()

        if resposta == 'sim':
            modulo = ModuloDecisao(orientacao)
            resultado = modulo.executar_interativo()

            self.registrar(
                pergunta=f'Verificação de elegibilidade: {orientacao.titulo}',
                origem='modulo_decisao',
                id_orientacao=orientacao.id_orientacao,
                encontrou='sim',
                ajudou='sim' if resultado == 1 else 'nao',
                tentativa=1,
                tempo=0
            )

            input('\nPressione ENTER para continuar...')
            apagar_terminal()

    def registrar(self, pergunta, origem, id_orientacao, encontrou, ajudou, tentativa, tempo):
        registro = {
            'data': time.strftime('%Y-%m-%d %H:%M:%S'),
            'origem': origem,
            'pergunta': pergunta,
            'id_orientacao': id_orientacao,
            'encontrou': encontrou,
            'ajudou': ajudou,
            'tentativa': tentativa,
            'tempo': tempo,
        }
        self.historico.append(registro)
        self.exportar_csv(['data', 'origem', 'pergunta', 'id_orientacao', 'encontrou', 'ajudou', 'tentativa', 'tempo'])

    def exportar_csv(self, colunas):
        os.makedirs('data', exist_ok=True)
        caminho = 'data/historico.csv'

        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline().strip()
                if primeira_linha.split(';') != colunas:
                    print('Aviso: Estrutura do histórico mudou. Recriando arquivo...')
                    os.remove(caminho)

        arquivo_existe = os.path.exists(caminho)
        with open(caminho, mode="a", newline="", encoding="utf-8") as historico:
            escritor = csv.DictWriter(historico, fieldnames=colunas, delimiter=";")
            if not arquivo_existe:
                escritor.writeheader()
            escritor.writerows(self.historico)
            self.historico.clear()

    def indicadores(self):
        try:
            with open('data/historico.csv', 'r', encoding='utf-8') as historico:
                registros = list(csv.DictReader(historico, delimiter=';'))
        except FileNotFoundError:
            print('Arquivo histórico não encontrado.')
            return "Nenhum histórico encontrado."

        notas_arquivo = []
        try:
            with open('data/notas.csv', 'r', encoding='utf-8') as arquivo_notas:
                leitor_notas = csv.DictReader(arquivo_notas, delimiter=';')
                for linha in leitor_notas:
                    if linha.get('nota') and str(linha['nota']).strip().isdigit():
                        notas_arquivo.append(int(linha['nota']))
        except FileNotFoundError:
            notas_arquivo = []

        cont_ajudou = 0
        cont_encontrou = 0
        total_perguntas = 0
        tempo_total = 0
        cont_tentativas = 0
        perguntas_sem_solucao_csv = []
        for registro in registros:
            total_perguntas += 1
            tempo_total += float(registro['tempo'])
            cont_tentativas += int(registro['tentativa'])
            if registro['ajudou'] == 'sim':
                cont_ajudou += 1
            if registro['encontrou'] == 'sim':
                cont_encontrou += 1
            else:
                perguntas_sem_solucao_csv.append(registro['pergunta'])

        if total_perguntas == 0:
            return "Nenhum atendimento registrado."

        porcentagem_respostas_ajudadas = (cont_ajudou / total_perguntas) * 100
        porcentagem_respostas_encontradas = (cont_encontrou / total_perguntas) * 100
        tempo_medio = tempo_total / total_perguntas
        tentativas_por_atendimento = cont_tentativas / total_perguntas

        if notas_arquivo:
            facilidade_uso = sum(notas_arquivo) / len(notas_arquivo)
        elif self.notas_sessao:
            facilidade_uso = sum(self.notas_sessao) / len(self.notas_sessao)
        else:
            facilidade_uso = 0

        relatorio = [
            porcentagem_respostas_ajudadas,
            porcentagem_respostas_encontradas,
            tempo_medio,
            tentativas_por_atendimento,
            facilidade_uso,
            self.perguntas_sem_solucao_sessao,
        ]
        return relatorio

    def salvar_nota(self, nota):
        os.makedirs('data', exist_ok=True)
        arquivo_existe = os.path.exists('data/notas.csv')
        with open('data/notas.csv', mode='a', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            if not arquivo_existe:
                escritor.writerow(['data', 'nota'])
            escritor.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), nota])