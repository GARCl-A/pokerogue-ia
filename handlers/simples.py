"""Handlers para telas simples que apenas confirmam com ENTER."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla

TELAS_CONFIRMAR = {"OPTION_SELECT", "SAVE_SLOT", "MESSAGE"}


def handle_confirmar(dados: dict, agent) -> dict:
    """Aperta ENTER em telas de confirmação genéricas."""
    return acao(Tecla.ENTER.value)
