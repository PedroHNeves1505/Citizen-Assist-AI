import csv
from .utils import normalizar
from .orientacao import Orientacao
class BaseConhecimento():
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []
        
    def carregar(self):
        try:    
            self.orientacoes.clear()
            with open(self.caminho, 'r', encoding="utf-8") as base_conhecimento:
                leitor = csv.DictReader(base_conhecimento, delimiter=';')
                for linha in leitor:
                    
                    id_bruto = linha.get('id_orientacao')
                    
                    if not id_bruto or not str(id_bruto).strip().isdigit(): 
                        continue
                    
                    orientacao = Orientacao(
                        int(id_bruto.strip()),
                        linha.get('categoria', 'Sem Categoria'),
                        linha.get('titulo', 'Sem Titulo'),
                        linha.get('palavras_chave', 'Sem Palavras-chave'),
                        linha.get('resposta', 'Sem Resposta'),
                        linha.get('documentos', 'Sem Documentos'),
                        linha.get('onde', 'Nao informado'),
                        linha.get('fonte', 'Sem Fonte'),
                        linha.get('verificado_em', 'Sem Data'),
                        linha.get('expressao_booleana', 'Sem expressão').strip(),
                    )
                    self.orientacoes.append(orientacao)
        except FileNotFoundError:
            print('Arquivo não encontrado!')
        except csv.Error as e:
            print(f'Erro: {e}')
        return self.orientacoes
    
    def categorias(self):
        lista_categorias = []
        for orientacao in self.orientacoes:
            categorias_orientacao = [categoria.strip() for categoria in orientacao.categoria.split('|')]
            for categoria in categorias_orientacao:
                if categoria not in lista_categorias:
                    lista_categorias.append(categoria)
        return sorted(lista_categorias)
        
    def por_categoria(self, categoria_escolhida):
        orientacoes_selecionadas = []
        for orientacao in self.orientacoes:
            categorias_orientacao = [categoria.strip().lower() for categoria in orientacao.categoria.split('|')]
            if categoria_escolhida.lower() in categorias_orientacao:
                orientacoes_selecionadas.append(orientacao)
        return orientacoes_selecionadas
                
    
    def buscar(self, pergunta):
        pergunta_normalizada = normalizar(pergunta)
        pergunta_lista = pergunta_normalizada.split()
        resultados = []

        for orientacao in self.orientacoes:
            pontos = 0

            palavras_chave_limpas = [palavra.strip() for palavra in normalizar(orientacao.palavras_chave).split("|")]
            for palavra in palavras_chave_limpas:
                if len(palavra) < 3:
                    continue

                if palavra in pergunta_lista:
                    pontos += 3
                    continue

                if len(palavra) >= 4:
                    for word in pergunta_lista:
                        if len(word) < 4:
                            continue

                        prefixo = 0
                        for p1, p2 in zip(palavra, word):
                            if p1 == p2:
                                prefixo += 1
                            else:
                                break
                        if prefixo >= 4:
                            pontos += 2
                            break

                        if palavra in word or word in palavra:
                            pontos += 1
                            break

            titulo_limpo = normalizar(orientacao.titulo).split()
            for palavra_titulo in titulo_limpo:
                if len(palavra_titulo) < 4:
                    continue

                if palavra_titulo in pergunta_lista:
                    pontos += 1
                    continue

                for palavra_pergunta in pergunta_lista:
                    if len(palavra_pergunta) < 4:
                        continue
                    prefixo = 0
                    for p1, p2 in zip(palavra_titulo, palavra_pergunta):
                        if p1 == p2:
                            prefixo += 1
                        else:
                            break
                    if prefixo >= 4:
                        pontos += 0.5
                        break
                    if palavra_titulo in palavra_pergunta or palavra_pergunta in palavra_titulo:
                        pontos += 0.5
                        break

            if pontos > 0:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda x: x[0], reverse=True)
        return resultados