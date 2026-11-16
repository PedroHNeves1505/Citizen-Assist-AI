class Orientacao():
    def __init__(self, id_orientacao, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em, expressao_booleana=""):
        self.id_orientacao = id_orientacao
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        self.expressao_booleana = expressao_booleana

    def exibir(self):
        print('-' * 50)
        print(f'>> {self.titulo} [{self.categoria}]')
        print(f'\n{self.resposta}')

        print('\nDocumentos Necessários:')
        if self.documentos and self.documentos.strip():
            for documento in str(self.documentos).split('|'):
                print(f' - {documento.strip()}')
        else:
            print(' - Nenhum documento necessário.')

        print(f'\nOnde: {self.onde}')
        print(f'Fonte: {self.fonte} | Verificado em: {self.verificado_em}')
        print('\nAviso: este assistente NÃO é um canal oficial!')
        print('-' * 50 + '\n')