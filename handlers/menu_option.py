"""Handler para menus de opções genéricos (OPTION_SELECT e MENU_OPTION_SELECT)."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_menu_option(dados: dict, agent) -> dict | None:
    """Navega no menu de opções. Por padrão, escolhe a primeira opção para manter o jogo rodando."""
    opcoes = dados.get("opcoes", [])
    cursor_atual = dados.get("cursor", 0)

    print(f"📋 Menu de Opções aberto! Opções disponíveis: {opcoes}")

    # O alvo padrão para manter o bot fluindo é sempre a opção 0 (Carregar / Novo Jogo)
    alvo = 0

    # Se por algum motivo o menu estiver vazio, aperta B/X para tentar cancelar
    if not opcoes:
        return acao(Tecla.X.value)

    if cursor_atual == alvo:
        print(f"🎯 Cursor no alvo ({alvo}: '{opcoes[alvo]}')! Confirmando com ESPAÇO!")
        return acao(Tecla.ESPACO.value)

    # Navegação vertical simples
    if cursor_atual < alvo:
        print(f"🧭 Descendo o cursor ({cursor_atual} -> {alvo})...")
        return acao(Tecla.BAIXO.value)
    else:
        print(f"🧭 Subindo o cursor ({cursor_atual} -> {alvo})...")
        return acao(Tecla.CIMA.value)
