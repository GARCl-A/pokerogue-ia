"""Handler para a tela de seleção de ataque (FIGHT)."""

import importlib
from agent import Agent
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla


def handle_fight(dados: dict, agent: Agent) -> dict | None:
    """Decide o melhor MoveID e navega o cursor até o índice correto dele."""
    golpes = dados.get("golpes", [])
    cursor_atual = dados.get("cursor", 0)
    estado_atual = agent.memoria.estado_atual or "Desconhecido"

    if not golpes:
        return None

    # 1. CÉREBRO PENSA — O Cérebro avalia qual o melhor MoveID para usar
    if agent.memoria.ataque_alvo_indice is None:
        golpe_escolhido = agent.escolher_ataque(estado_atual, golpes)

        # As mãos precisam saber o ÍNDICE para se mover
        agent.memoria.ataque_alvo_indice = golpe_escolhido["indice"]

        # O Q-Learning precisa do ID do ataque para salvar na Tabela Q
        agent.registrar_acao(estado_atual, golpe_escolhido["id"])

    # 2. MÃOS EXECUTAM — navega o cursor até o índice alvo
    alvo_indice = agent.memoria.ataque_alvo_indice

    if cursor_atual == alvo_indice:
        print(f"🎯 Cursor posicionado no slot {alvo_indice}! Disparando ESPAÇO!")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESPACO.value)

    tecla_mov = tecla_para_alvo(cursor_atual, alvo_indice)
    print(f"🧭 Movendo o cursor do slot {cursor_atual} para {alvo_indice}...")
    return acao(tecla_mov)
