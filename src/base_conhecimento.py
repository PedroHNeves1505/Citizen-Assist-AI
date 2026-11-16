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
                        id_orientacao=int(str(id_bruto).strip()),
                        categoria=linha.get('categoria', 'Sem Categoria'),
                        titulo=linha.get('titulo', 'Sem Titulo'),
                        palavras_chave=linha.get('palavras_chave', 'Sem Palavras-chave'),
                        resposta=linha.get('resposta', 'Sem Resposta'),
                        documentos=linha.get('documentos', 'Sem Documentos'),
                        onde=linha.get('onde', 'Nao informado'),
                        fonte=linha.get('fonte', 'Sem Fonte'),
                        verificado_em=linha.get('verificado_em', 'Sem Data'),
                        expressao_booleana=linha.get('expressao_booleana', '').strip(),
                    )
                    self.orientacoes.append(orientacao)
        except FileNotFoundError:
            print('Aviso: Arquivo de base de conhecimento não encontrado!')
        except csv.Error as e:
            print(f'Erro ao ler o formato do CSV: {e}')
        except Exception as e:
            print(f'Erro inesperado: {e}')
        return self.orientacoes

    def categorias(self):
        categorias_unicas = []
        for orientacao in self.orientacoes:
            categorias_orientacao = [cat.strip() for cat in orientacao.categoria.split('|')]
            for cat in categorias_orientacao:
                if cat and cat not in categorias_unicas:
                    categorias_unicas.append(cat)
        return sorted(categorias_unicas)

    def por_categoria(self, categoria_escolhida):
        orientacoes_selecionadas = []
        for orientacao in self.orientacoes:
            categorias_orientacao = [c.strip().lower() for c in orientacao.categoria.split('|')]
            if categoria_escolhida.lower() in categorias_orientacao:
                orientacoes_selecionadas.append(orientacao)
        return orientacoes_selecionadas

    def buscar(self, pergunta):
        pergunta_normalizada = normalizar(pergunta)
        pergunta_lista = pergunta_normalizada.split()
        resultados = []

        for orientacao in self.orientacoes:
            pontos = 0

            palavras_chave_limpas = [p.strip() for p in normalizar(orientacao.palavras_chave).split("|")]
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
                        for c1, c2 in zip(palavra, word):
                            if c1 == c2:
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
            for word_titulo in titulo_limpo:
                if len(word_titulo) < 4:
                    continue
                if word_titulo in pergunta_lista:
                    pontos += 1
                    continue
                for word_pergunta in pergunta_lista:
                    if len(word_pergunta) < 4:
                        continue
                    prefixo = 0
                    for c1, c2 in zip(word_titulo, word_pergunta):
                        if c1 == c2:
                            prefixo += 1
                        else:
                            break
                    if prefixo >= 4:
                        pontos += 0.5
                        break
                    if word_titulo in word_pergunta or word_pergunta in word_titulo:
                        pontos += 0.5
                        break

            if pontos > 0:
                resultados.append((pontos, orientacao))

        resultados.sort(key=lambda x: x[0], reverse=True)
        return resultados