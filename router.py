"""Roteador de telas: mapeia nome_tela para o handler correspondente."""

from typing import Callable, Optional
from agent import Agent
from handlers.simples import handle_confirmar, TELAS_CONFIRMAR
from handlers.title import handle_title
from handlers.starter import handle_starter_select
from handlers.fight import handle_fight
from handlers.command import handle_command
from handlers.loot import handle_loot
from handlers.party import handle_party, handle_target_select
from handlers.summary import handle_summary
from handlers.menu_option import handle_menu_option
from handlers.confirm import handle_confirm

HandlerFn = Callable[[dict, Agent], Optional[dict]]

_ROTAS: dict[str, HandlerFn] = {
    "TITLE": handle_title,
    "STARTER_SELECT": handle_starter_select,
    "FIGHT": handle_fight,
    "COMMAND": handle_command,
    "CONFIRM": handle_confirm,
    "TARGET_SELECT": handle_target_select,
    "MODIFIER_SELECT": handle_loot,
    "PARTY": handle_party,
    "SUMMARY": handle_summary,
    "OPTION_SELECT": handle_menu_option,
    "MENU_OPTION_SELECT": handle_menu_option,
}

# Registra todas as telas de confirmação simples no mesmo handler
for _tela in TELAS_CONFIRMAR:
    _ROTAS[_tela] = handle_confirmar


def rotear(nome_tela: str, dados: dict, agent: Agent) -> Optional[dict]:
    """Delega o processamento da tela ao handler registrado. Retorna None se a tela for desconhecida."""
    handler = _ROTAS.get(nome_tela)
    if handler is None:
        return None
    return handler(dados, agent)
