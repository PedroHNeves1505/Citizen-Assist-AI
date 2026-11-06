class Orientacao():
    def __init__(self, id_orientacao:int, categoria:str, titulo:str, palavras_chave:str, resposta:str, documentos:str, onde:str, fonte:str, verificado_em:str):
        self.id_orientacao = id_orientacao
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
    
    def exibir(self):
        print('-' * 40)
        print(f'\n{self.titulo} [{self.categoria}]')
        print(self.resposta)
        print('Documentos Necessários:')
        if self.documentos:
            for documento in str(self.documentos).split('|'):
                print(f' - {documento.strip()}')
        else:
            print(' - Nenhum Documento Necessário')
        print(f'Onde: {self.onde}')
        print(f'Fonte: {self.fonte} | verificado em: {self.verificado_em}\n')
        print('Aviso: este assistente NÃO é um canal oficial!\n')
        print('-' * 40)