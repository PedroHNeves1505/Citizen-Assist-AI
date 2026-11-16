"""
Citizen Assist AI - Gerenciador de Orientações (Data Structures and Algorithms)
Integrado ao base_conhecimento.csv do assistente.
Estrutura: lista encadeada simples (No + ListaEncadeada), implementada pela equipe.
"""
import csv
import os
import re
import unicodedata
from dataclasses import dataclass

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_CSV = os.path.join(PASTA_PROJETO, "data", "base_conhecimento.csv")

CAMPOS = [
    "id_orientacao", "categoria", "titulo", "palavras_chave",
    "resposta", "documentos", "onde", "fonte",
    "verificado_em", "expressao_booleana",
]


@dataclass
class OrientacaoDSA:
    id_orientacao: int
    categoria: str
    titulo: str
    palavras_chave: str
    resposta: str
    documentos: str
    onde: str
    fonte: str
    verificado_em: str
    expressao_booleana: str = ""


def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


# ----------------------------------------------------------------------
# Lista encadeada
# ----------------------------------------------------------------------
class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def __len__(self):
        return self.tamanho

    def esta_vazia(self):
        return self.inicio is None

    def __iter__(self):
        atual = self.inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    def inserir_inicio(self, dado):
        novo = No(dado)
        novo.proximo = self.inicio
        self.inicio = novo
        if self.fim is None:
            self.fim = novo
        self.tamanho += 1

    def inserir_fim(self, dado):
        novo = No(dado)
        if self.fim is None:
            self.inicio = novo
        else:
            self.fim.proximo = novo
        self.fim = novo
        self.tamanho += 1

    def buscar_por_id(self, id_):
        for dado in self:
            if dado.id_orientacao == id_:
                return dado
        return None

    def pesquisar(self, texto, campo=None):
        termos = normalizar(texto).split()
        resultado = ListaEncadeada()
        if not termos:
            return resultado
        for dado in self:
            if campo:
                alvo = normalizar(getattr(dado, campo))
            else:
                alvo = normalizar(" ".join([
                    dado.titulo, dado.categoria,
                    dado.palavras_chave, dado.resposta
                ]))
            if all(t in alvo for t in termos):
                resultado.inserir_fim(dado)
        return resultado

    def atualizar(self, id_, **novos_valores):
        dado = self.buscar_por_id(id_)
        if dado is None:
            return False
        for campo, valor in novos_valores.items():
            if campo != "id_orientacao" and hasattr(dado, campo):
                setattr(dado, campo, valor)
        return True

    def remover_por_id(self, id_):
        anterior = None
        atual = self.inicio
        while atual is not None:
            if atual.dado.id_orientacao == id_:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self.fim:
                    self.fim = anterior
                atual.proximo = None
                self.tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    # ---- Merge Sort próprio ----
    def ordenar(self, chave, reverso=False):
        self.inicio = self._merge_sort(self.inicio, chave, reverso)
        self.fim = None
        atual = self.inicio
        while atual is not None:
            self.fim = atual
            atual = atual.proximo

    def _dividir(self, cabeca):
        lento = cabeca
        rapido = cabeca.proximo
        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo
        meio = lento.proximo
        lento.proximo = None
        return meio

    def _merge_sort(self, cabeca, chave, reverso):
        if cabeca is None or cabeca.proximo is None:
            return cabeca
        meio = self._dividir(cabeca)
        esquerda = self._merge_sort(cabeca, chave, reverso)
        direita = self._merge_sort(meio, chave, reverso)
        return self._mesclar(esquerda, direita, chave, reverso)

    def _mesclar(self, a, b, chave, reverso):
        sentinela = No(None)
        cauda = sentinela
        while a is not None and b is not None:
            ka, kb = chave(a.dado), chave(b.dado)
            pegar_a = ka >= kb if reverso else ka <= kb
            if pegar_a:
                cauda.proximo, a = a, a.proximo
            else:
                cauda.proximo, b = b, b.proximo
            cauda = cauda.proximo
        cauda.proximo = a if a is not None else b
        return sentinela.proximo

    def contar_por_categoria(self):
        contagem = {}
        for dado in self:
            categorias = [c.strip() for c in dado.categoria.split("|") if c.strip()]
            for cat in categorias:
                contagem[cat] = contagem.get(cat, 0) + 1
        return contagem

    def proximo_id(self):
        maior = 0
        for dado in self:
            if dado.id_orientacao > maior:
                maior = dado.id_orientacao
        return maior + 1


# ----------------------------------------------------------------------
# Persistência
# ----------------------------------------------------------------------
def carregar_csv(lista, caminho=ARQUIVO_CSV):
    carregados = ignorados = 0
    if not os.path.exists(caminho):
        return 0, 0
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f, delimiter=";"):
            try:
                reg = OrientacaoDSA(
                    id_orientacao=int(linha["id_orientacao"]),
                    categoria=linha["categoria"].strip(),
                    titulo=linha["titulo"].strip(),
                    palavras_chave=linha["palavras_chave"].strip(),
                    resposta=linha["resposta"].strip(),
                    documentos=linha.get("documentos", "").strip(),
                    onde=linha.get("onde", "").strip(),
                    fonte=linha.get("fonte", "").strip(),
                    verificado_em=linha.get("verificado_em", "").strip(),
                    expressao_booleana=linha.get("expressao_booleana", "").strip(),
                )
            except (KeyError, ValueError, AttributeError):
                ignorados += 1
                continue
            if not reg.titulo or lista.buscar_por_id(reg.id_orientacao) is not None:
                ignorados += 1
                continue
            lista.inserir_fim(reg)
            carregados += 1
    return carregados, ignorados


def salvar_csv(lista, caminho=ARQUIVO_CSV):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        escritor.writeheader()
        for reg in lista:
            escritor.writerow({c: getattr(reg, c) for c in CAMPOS})


# ----------------------------------------------------------------------
# Validação
# ----------------------------------------------------------------------
PADROES_DADOS_PESSOAIS = [
    re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
]


def contem_dado_pessoal(texto):
    return any(p.search(texto) for p in PADROES_DADOS_PESSOAIS)


def ler_inteiro(mensagem, minimo=1):
    while True:
        entrada = input(mensagem).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("  Entrada inválida: digite apenas números inteiros.")
            continue
        if valor < minimo:
            print(f"  O número deve ser maior ou igual a {minimo}.")
            continue
        return valor


def ler_texto(mensagem, obrigatorio=True, atual=None):
    while True:
        entrada = input(mensagem).strip()
        if not entrada and atual is not None:
            return atual
        if not entrada and not obrigatorio:
            return ""
        if obrigatorio and not entrada:
            print("  Campo obrigatório: não pode ficar vazio.")
            continue
        if contem_dado_pessoal(entrada):
            print("  Atenção: parece haver CPF ou e-mail. Não cadastre dados pessoais.")
            continue
        return entrada


# ----------------------------------------------------------------------
# Exibição
# ----------------------------------------------------------------------
def mostrar(reg, resumido=False):
    if resumido:
        print(f"  [{reg.id_orientacao:>3}] {reg.titulo}  ({reg.categoria})")
        return
    print("\n" + "-" * 62)
    print(f"ASSUNTO: {reg.titulo}")
    print(f"Tema: {reg.categoria}")
    print("\nO QUE VOCÊ PODE FAZER:")
    print(f"{reg.resposta}")
    if reg.documentos:
        print(f"\nDocumentos necessários: {reg.documentos.replace('|', ', ')}")
    if reg.onde:
        print(f"Onde: {reg.onde}")
    print(f"\nFonte: {reg.fonte}")
    print(f"Última atualização: {reg.verificado_em}")
    print("-" * 62)


def listar(lista, resumido=True):
    if lista.esta_vazia():
        print("  Ainda não há orientações cadastradas.")
        return
    for reg in lista:
        mostrar(reg, resumido)
    print(f"\nTotal de orientações: {len(lista)}")


# ----------------------------------------------------------------------
# Menu do cidadão / pesquisa
# ----------------------------------------------------------------------
def consultar_por_assunto(lista):
    print("\n-- Sobre qual assunto você precisa de ajuda? --")
    categorias = list(lista.contar_por_categoria().keys())
    if not categorias:
        print("Ainda não há assuntos cadastrados.")
        return
    for numero, categoria in enumerate(categorias, start=1):
        print(f"{numero}) {categoria}")
    print("0) Voltar")
    opcao = ler_inteiro("Digite o número do assunto: ", minimo=0)
    if opcao == 0:
        return
    if opcao > len(categorias):
        print("Essa opção não existe. Tente novamente.")
        return
    categoria_escolhida = categorias[opcao - 1]
    achados = ListaEncadeada()
    for reg in lista:
        cats = [c.strip() for c in reg.categoria.split("|")]
        if categoria_escolhida in cats:
            achados.inserir_fim(reg)
    print(f"\nOrientações sobre {categoria_escolhida}:")
    listar(achados, resumido=False)


def pesquisar_por_palavra(lista):
    """Mostra palavras-chave únicas e permite escolher uma para buscar (lista encadeada)."""
    print("\n-- Pesquisar orientação --")
    palavras = []
    for reg in lista:
        for palavra in reg.palavras_chave.split("|"):
            palavra = palavra.strip()
            if palavra and palavra not in palavras:
                palavras.append(palavra)

    if not palavras:
        print("  Nenhuma palavra-chave cadastrada.")
        return

    palavras.sort()
    print("\nEscolha uma palavra para pesquisar:")
    for i, palavra in enumerate(palavras, start=1):
        print(f"  {i:>2}) {palavra}")
    print("   0) Voltar")

    opcao = ler_inteiro("Digite o número da palavra: ", minimo=0)
    if opcao == 0:
        return
    if opcao > len(palavras):
        print("  Opção inválida.")
        return

    palavra_escolhida = palavras[opcao - 1]
    achados = lista.pesquisar(palavra_escolhida)

    if achados.esta_vazia():
        print(f"\n  Nenhuma orientação encontrada para '{palavra_escolhida}'.")
    else:
        print(f"\n  Orientações com '{palavra_escolhida}':")
        listar(achados, resumido=False)


def ordenar(lista):
    print("\n-- Organizar orientações (Merge Sort) --")
    if lista.esta_vazia():
        print("  A lista está vazia.")
        return
    print("  1) Número   2) Título   3) Assunto")
    op = ler_inteiro("Escolha como organizar: ")
    chaves = {
        1: lambda r: r.id_orientacao,
        2: lambda r: normalizar(r.titulo),
        3: lambda r: normalizar(r.categoria),
    }
    if op not in chaves:
        print("  Opção inexistente.")
        return
    desc = input("  Ordem inversa? (s/n): ").strip().lower() == "s"
    lista.ordenar(chaves[op], reverso=desc)
    listar(lista)


# ----------------------------------------------------------------------
# CRUD (mantido na classe, fora do menu do assistente)
# ----------------------------------------------------------------------
def cadastrar(lista):
    print("\n-- Cadastrar nova orientação (equipe) --")
    sugestao = lista.proximo_id()
    while True:
        id_ = ler_inteiro(f"ID (sugestão {sugestao}): ")
        if lista.buscar_por_id(id_) is not None:
            print("  Esse ID já existe. Escolha outro.")
        else:
            break
    reg = OrientacaoDSA(
        id_orientacao=id_,
        categoria=ler_texto("Categoria (separadas por |): "),
        titulo=ler_texto("Título: "),
        palavras_chave=ler_texto("Palavras-chave (separadas por |): "),
        resposta=ler_texto("Resposta: "),
        documentos=ler_texto("Documentos (separados por |, opcional): ", obrigatorio=False),
        onde=ler_texto("Onde (opcional): ", obrigatorio=False),
        fonte=ler_texto("Fonte (URL): "),
        verificado_em=ler_texto("Verificado em (YYYY-MM-DD): "),
        expressao_booleana=ler_texto("Expressão booleana (opcional): ", obrigatorio=False),
    )
    lista.inserir_fim(reg)
    print("  Orientação cadastrada.")


def consultar(lista):
    print("\n-- Consultar registro por ID --")
    if lista.esta_vazia():
        print("  A lista está vazia.")
        return
    reg = lista.buscar_por_id(ler_inteiro("ID: "))
    if reg is None:
        print("  Nenhum registro encontrado com esse ID.")
    else:
        mostrar(reg)


def atualizar(lista):
    print("\n-- Atualizar orientação (equipe) --")
    reg = lista.buscar_por_id(ler_inteiro("ID do registro: "))
    if reg is None:
        print("  Registro inexistente.")
        return
    print("  (Pressione Enter para manter o valor atual)")
    lista.atualizar(
        reg.id_orientacao,
        categoria=ler_texto(f"Categoria [{reg.categoria}]: ", atual=reg.categoria),
        titulo=ler_texto(f"Título [{reg.titulo}]: ", atual=reg.titulo),
        palavras_chave=ler_texto(f"Palavras-chave [{reg.palavras_chave}]: ", atual=reg.palavras_chave),
        resposta=ler_texto(f"Resposta [{reg.resposta[:40]}...]: ", atual=reg.resposta),
        documentos=ler_texto(f"Documentos [{reg.documentos}]: ", atual=reg.documentos, obrigatorio=False),
        onde=ler_texto(f"Onde [{reg.onde}]: ", atual=reg.onde, obrigatorio=False),
        fonte=ler_texto(f"Fonte [{reg.fonte}]: ", atual=reg.fonte),
        verificado_em=ler_texto(f"Verificado em [{reg.verificado_em}]: ", atual=reg.verificado_em),
        expressao_booleana=ler_texto(f"Expressão [{reg.expressao_booleana}]: ", atual=reg.expressao_booleana, obrigatorio=False),
    )
    print("  Orientação atualizada.")


def excluir(lista):
    print("\n-- Excluir orientação (equipe) --")
    reg = lista.buscar_por_id(ler_inteiro("ID do registro: "))
    if reg is None:
        print("  Registro inexistente.")
        return
    mostrar(reg, resumido=True)
    if input("  Confirma a exclusão? (s/n): ").strip().lower() == "s":
        lista.remover_por_id(reg.id_orientacao)
        print("  Orientação excluída.")
    else:
        print("  Exclusão cancelada.")


# ----------------------------------------------------------------------
# Classe encapsuladora para o assistente
# ----------------------------------------------------------------------
class GerenciadorOrientacoes:
    def __init__(self, caminho=ARQUIVO_CSV):
        self.caminho = caminho
        self.lista = ListaEncadeada()
        self.carregar()

    def carregar(self):
        return carregar_csv(self.lista, self.caminho)

    def salvar(self):
        salvar_csv(self.lista, self.caminho)

    # Exposição para o menu
    def pesquisar(self):
        pesquisar_por_palavra(self.lista)

    def ordenar(self):
        ordenar(self.lista)

    def listar(self):
        listar(self.lista, resumido=False)

    # CRUD disponível para uso futuro
    def cadastrar(self):
        cadastrar(self.lista)
        self.salvar()

    def consultar(self):
        consultar(self.lista)

    def atualizar(self):
        atualizar(self.lista)
        self.salvar()

    def excluir(self):
        excluir(self.lista)
        self.salvar()


if __name__ == "__main__":
    from .utils import apagar_terminal
    ger = GerenciadorOrientacoes()
    while True:
        print("\n=== GERENCIADOR (uso isolado) ===")
        print("1) Pesquisar  2) Ordenar  3) Listar  0) Sair")
        op = ler_inteiro("Escolha: ", minimo=0)
        if op == 0:
            break
        elif op == 1:
            ger.pesquisar()
        elif op == 2:
            ger.ordenar()
        elif op == 3:
            ger.listar()
        input("Pressione ENTER...")
        apagar_terminal()