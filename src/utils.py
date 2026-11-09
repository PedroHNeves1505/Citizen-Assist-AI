import os

ACENTOS = {
    "á": "a",
    "à": "a",
    "ã": "a",
    "â": "a",
    "é": "e",
    "ê": "e",
    "í": "i",
    "ó": "o",
    "õ": "o",
    "ô": "o",
    "ú": "u",
    "ç": "c"
    }

def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "

def apagar_terminal():
    input('Aperte qualquer botão para continuar.')
    os.system("cls" if os.name == "nt" else "clear")