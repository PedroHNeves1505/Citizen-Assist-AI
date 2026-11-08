import re
from base_conhecimento import BaseConhecimento
from utils import apagar_terminal
import sys
import time
import csv
import os
from orientacao import Orientacao

class Assistente():
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.notas_sessao = []
        
    def menu(self):
        while True:
            print(f'Bem Vindo ao {self.nome}')
            print(f'\n{"-" * 40}')
            print('Você tem alguma pergunta ou prefere olhar as categorias?')
            print('1. Pergunta')
            print('2. Categorias')
            print('0. Sair')
            print(f'{"-" * 40}\n')
            try:
                escolha = int(input('Digite o valor da opção desejada: '))
            except ValueError:
                print('Atenção: opção inválida! Tente novamente.')
                apagar_terminal()
                continue
            if escolha not in [0, 1, 2]:
                print('Atenção: opção inválida! Tente novamente.')
                apagar_terminal()
                continue
            else:
                break
            
        match escolha:
            case 0:
                print('Saindo do sistema!')
                try:
                    nota = int(input('\nComo você pontua a facilidade do programa? De 1 a 5: '))
                    if 1 <= nota <= 5:
                        self.notas_sessao.append(nota)
                        self.salvar_nota(nota)
                    else:
                        self.notas_sessao.append(0)
                        self.salvar_nota(0)
                except ValueError:
                    self.notas_sessao.append(0)
                    self.salvar_nota(0)
                print('Obrigado pelo retorno!')
                time.sleep(2)
                sys.exit()
            case 1:
                self.perguntar()
            case 2:
                self.navegar()
    
    def perguntar(self):        
        padrao_cpf_ou_telefone = r"(\b\d{3}[\.\s-]?\d{3}[\.\s-]?\d{3}[\.\s-]?\d{2}\b)|(\b(?:\+?55\s*)?(?:\(\d{2}\)|\d{2})[\s.-]?\d{4,5}[\s.-]?\d{4}\b)"
        while True:
            pergunta = input('Digite a sua dúvida: ')
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
            self.registrar(pergunta, 'pergunta', 'N/A', 'nao', 'nao', 1, tempo)
            apagar_terminal()
            return 
        
        
        pontos, orientacao = resultados[0]
        if pontos >= 6: 
            print('Confiança ALTA')
        elif pontos >= 3: 
            print('Confiança MÉDIA')
        else: 
            print('Confiança BAIXA. Não encontrei uma resposta exata.')
            self.registrar(pergunta, 'pergunta', 'N/A', 'nao', 'nao', 1, tempo)
            return
        orientacao.exibir()
        
        ajudou = input('Essa orientação respondeu sua dúvida? (s/n): ').lower()
        while ajudou not in ['s', 'n']:
            ajudou = input('Digite apenas s ou n: ').lower()
            
        self.registrar(
            pergunta=pergunta,
            origem='categoria',
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
                    return
                elif id_categoria_escolhida not in opcoes_possiveis:
                    print('\nAviso: Digite uma valor dentro da sequência!')
                    apagar_terminal()
                    continue
                break
            except ValueError:
                print('\nAviso: Digite uma valor dentro da sequência!')
                continue
        
        inicio = time.time()
                
        lista_categoria = self.base.categorias()
        categoria_escolhida = lista_categoria[id_categoria_escolhida - 1]
        lista = self.base.por_categoria(categoria_escolhida)
        
        while True:
            if not lista:
                print('Nenhuma orientação nesta categoria.')
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
                return
            try: 
                opcao = int(opcao_escolhida)
                if 1 <= opcao <= len(lista): 
                    tempo = round(time.time() - inicio, 1)
                    self.registrar('Acesso por categoria', 'categoria', lista[opcao-1].id_orientacao, 'sim', 'sim', 1, 0)
                    lista[opcao-1].exibir()
                    ajudou = input('Essa orientação respondeu sua dúvida? (s/n): ').lower()
                    while ajudou not in ['s', 'n']:
                        ajudou = input('Digite apenas s ou n: ').lower()
                        
                    self.registrar(
                        pergunta=f'Navegação por categoria: {categoria_escolhida} -> {lista[opcao-1].titulo}',
                        origem='categoria',
                        id_orientacao=lista[opcao-1].id_orientacao,
                        encontrou='sim',
                        ajudou=ajudou,
                        tentativa=1,
                        tempo=tempo
                    )
                    apagar_terminal()
                    inicio = time.time()
                else:
                    print('Opção inválida! Tente novamente.')
                    apagar_terminal()
                    continue
            except ValueError:
                print(f'Valor indisponível. Tente um valor entre 0 e {cont}')
                apagar_terminal()
                continue

    
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
        arquivo_existe = os.path.exists('data/historico.csv')
        
        with open('data/historico.csv', mode="a", newline="", encoding="utf-8") as historico:
            escritor = csv.DictWriter(historico, fieldnames=colunas, delimiter=";")
            
            if not arquivo_existe:
                escritor.writeheader()
                
            escritor.writerows(self.historico)
            self.historico.clear()
        
    def indicadores(self):
        try:
            with open('data/historico.csv', 'r') as historico: 
                registros = list(csv.DictReader(historico, delimiter=';'))
        except FileNotFoundError:
            print('Arquivo histórico não encontrado. Entre em contato com o suporte.')
            apagar_terminal()
            sys.exit()
            
        notas_arquivo = []
        try:
            with open('data/notas.csv', 'r', encoding='utf-8') as arquivo_notas:
                leitor_notas = csv.DictReader(arquivo_notas, delimiter=';')
                for linha in leitor_notas:
                    if str(linha['nota']).strip().isdigit():
                        notas_arquivo.append(int(linha['nota']))
                    
        except FileNotFoundError:
            notas_arquivo = []
        cont_ajudou = 0
        cont_encontrou = 0
        total_perguntas = 0
        tempo_total = 0
        cont_tentativas = 0
        perguntas_sem_solucao = []
        for registro in registros:
            total_perguntas += 1
            tempo_total += float(registro['tempo'])
            cont_tentativas += int(registro['tentativa'])
            if registro['ajudou'] == 'sim':
                cont_ajudou += 1
            if registro['encontrou'] == 'sim':
                cont_encontrou += 1
            else:
                perguntas_sem_solucao.append(registro['pergunta']) 
            
        if total_perguntas == 0:
            return "Nenhum atendimento registrado."
        else:
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
            perguntas_sem_solucao
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