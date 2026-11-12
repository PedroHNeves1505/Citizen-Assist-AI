from utils import normalizar

class ModuloDecisao():
    def __init__(self, orientacao_atual):
        self.orientacao_atual = orientacao_atual
        self.expressao_dividida = []
        self.variaveis = []
        self.valores_variavel = {}
        self.expressao_final = []
        self.resolucao = None
    
    def obter_expressao_booleana(self):
        expressao = self.orientacao_atual.expressao_booleana
        expressao = expressao.replace('(', ' ( ').replace(')', ' ) ')
        self.expressao_dividida = expressao.lower().strip().split()
        return self.expressao_dividida
    
    def obter_variaveis(self):
        operadores = {'and', 'or', 'not', '(', ')'}
        for item in self.expressao_dividida:
            if item not in operadores and item not in self.variaveis:
                self.variaveis.append(item)
        return self.variaveis
                
    def receber_valores_variaveis(self):
        for variavel in self.variaveis:
            while True:
                valor_variavel = input(f'Você tem {variavel.replace("_", " ")}?(sim ou não): ')
                valor_variavel = normalizar(valor_variavel).strip()
                if valor_variavel not in ['sim', 'nao']:
                    print('Digite apenas sim ou não. Tente novamente!')
                else:
                    if valor_variavel == 'sim':
                        valor_variavel = 1
                    else:
                        valor_variavel = 0
                    self.valores_variavel[variavel] = valor_variavel
                    break
        return self.valores_variavel
    
    def substituir_variavel_por_valor(self):
        self.expressao_final = []
        for token in self.expressao_dividida:
            if token in self.variaveis:
                self.expressao_final.append(str(self.valores_variavel[token]))
            else:
                self.expressao_final.append(token)
        return self.expressao_final
    
    def resolver_expressao(self):
        try: 
            self.resolucao = eval(' '.join(self.expressao_final), {}, {})
        except Exception as e:
            print(f'ERRO: {e}')
        return self.resolucao
        