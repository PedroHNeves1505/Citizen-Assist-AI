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
                    )
                    self.orientacoes.append(orientacao)
        except FileNotFoundError:
            print('Arquivo não encontrado!')
        except csv.Error as e:
            print(f'Erro: {e}')
        return self.orientacoes
    
    def categorias(self):
        categorias = [orientacao.categoria for orientacao in self.orientacoes]
        return sorted(set(categorias))
        
    def por_categoria(self, categoria_escolhida):
        orientacoes_selecionadas = []
        for orientacao in self.orientacoes:
            if orientacao.categoria.lower() == categoria_escolhida.lower():
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
                if len(palavra) >= 3 and palavra in pergunta_lista:
                    pontos += 3
                    
            titulo_limpo = normalizar(orientacao.titulo).split()
            for palavra in titulo_limpo:
                if len(palavra) >= 4 and palavra in pergunta_lista:
                    pontos += 1
                    
            if pontos > 0:
                resultados.append((pontos, orientacao))
                
        resultados.sort(key=lambda x: x[0], reverse=True)
        
        return resultados