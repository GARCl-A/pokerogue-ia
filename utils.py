"""Funções auxiliares compartilhadas entre os handlers."""
import importlib

Tecla = importlib.import_module("teclas").Tecla


def tecla_para_alvo(cursor_atual: int, alvo: int) -> int:
    """Retorna a tecla direcional necessária para mover o cursor de `cursor_atual` até `alvo` num grid 2x2."""
    linha_atual, col_atual = cursor_atual // 2, cursor_atual % 2
    linha_alvo, col_alvo = alvo // 2, alvo % 2
    if linha_atual < linha_alvo:
        return Tecla.BAIXO.value
    if linha_atual > linha_alvo:
        return Tecla.CIMA.value
    if col_atual < col_alvo:
        return Tecla.DIREITA.value
    return Tecla.ESQUERDA.value


def acao(tecla: int) -> dict:
    """Monta o payload de resposta padrão para apertar uma tecla."""
    return {"acao": "apertar", "tecla": tecla}
