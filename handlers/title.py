"""Handler para a tela de título (TITLE)."""
import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_title(dados: dict, agent) -> dict:
    """Navega o menu de título até encontrar 'New Game' / 'Novo Jogo' e confirma."""
    texto_opcao = dados.get("textoOpcao", "").upper()
    print(f"🤔 Lendo o menu. Opção atual: {texto_opcao}")

    if "NEW" in texto_opcao or "NOVO" in texto_opcao:
        print("✅ Achei o Novo Jogo! Começando...")
        return acao(Tecla.ENTER.value)

    print("➡️ Não é Novo Jogo. Descendo o cursor...")
    return acao(Tecla.BAIXO.value)
