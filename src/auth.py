"""
Autenticação simples para acesso restrito da equipe.
- Senha oculta com asteriscos (cross-platform, sem dependências externas)
- Hash SHA-256 (não armazena senha em texto puro)
- Limite de 3 tentativas
- Credenciais configuráveis via variáveis de ambiente

⚠️ Para produção real: usar bcrypt/argon2, 2FA, sessões, etc.
"""
import hashlib
import os
import sys


# Padrão para demonstração acadêmica:
#   usuário: equipe
#   senha:   fiap2026
# Em produção, defina CITIZEN_ADMIN_USER e CITIZEN_ADMIN_PASS no ambiente.
_USUARIO_PADRAO = "equipe"
_SENHA_PADRAO = "fiap2026"

MAX_TENTATIVAS = 3


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _credenciais_esperadas():
    usuario = os.environ.get("CITIZEN_ADMIN_USER", _USUARIO_PADRAO)
    senha = os.environ.get("CITIZEN_ADMIN_PASS", _SENHA_PADRAO)
    return _hash(usuario), _hash(senha)


# ----------------------------------------------------------------------
# Leitura de senha com asteriscos (cross-platform)
# ----------------------------------------------------------------------
def ler_senha(prompt: str = "Senha: ") -> str:
    """
    Lê uma senha exibindo '*' para cada caractere digitado.
    - Windows: usa msvcrt.getch()
    - Linux/macOS: usa termios + tty (desabilita eco)
    - Backspace funciona corretamente
    - Ctrl+C interrompe
    """
    print(prompt, end="", flush=True)
    senha = []

    if sys.platform == "win32":
        import msvcrt
        while True:
            char = msvcrt.getch()
            if char in (b"\r", b"\n"):
                print()
                break
            elif char in (b"\x08", b"\x7f"):  # backspace
                if senha:
                    senha.pop()
                    print("\b \b", end="", flush=True)
            elif char == b"\x03":  # Ctrl+C
                raise KeyboardInterrupt
            else:
                try:
                    letra = char.decode("utf-8")
                except UnicodeDecodeError:
                    letra = char.decode("latin-1")
                senha.append(letra)
                print("*", end="", flush=True)
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_attr = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ("\r", "\n"):
                    print()
                    break
                elif char in ("\x7f", "\x08"):
                    if senha:
                        senha.pop()
                        print("\b \b", end="", flush=True)
                elif char == "\x03":
                    raise KeyboardInterrupt
                else:
                    senha.append(char)
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)

    return "".join(senha)


def fazer_login() -> bool:
    """
    Solicita usuário e senha, compara com os hashes.
    Retorna True se autenticado, False após 3 tentativas.
    """
    usuario_hash, senha_hash = _credenciais_esperadas()

    print("\n" + "-" * 50)
    print("ACESSO RESTRITO — EQUIPE")
    print("-" * 50)

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        usuario = input("Usuário: ").strip()
        senha = ler_senha("Senha: ").strip()   

        if _hash(usuario) == usuario_hash and _hash(senha) == senha_hash:
            print("ACESSO: Login realizado com sucesso!")
            return True

        restantes = MAX_TENTATIVAS - tentativa
        if restantes > 0:
            print(f"ERRO: Credenciais inválidas. Tentativas restantes: {restantes}")

    print("FALHA: Número máximo de tentativas excedido.")
    return False