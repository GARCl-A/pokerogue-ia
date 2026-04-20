"""Handler para a tela de seleção de ataque (FIGHT)."""

import importlib
from agent import Agent
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla


def handle_fight(dados: dict, agent: Agent) -> dict | None:
    golpes = dados.get("golpes", [])
    cursor_atual = dados.get("cursor", 0)

    est_especifico = agent.memoria.estado_especifico_atual or "Desconhecido"
    est_geral = agent.memoria.estado_geral_atual or "T_Desconhecido"

    if not golpes:
        return None

    if agent.memoria.ataque_alvo_indice is None:
        golpe_escolhido = agent.escolher_ataque(est_especifico, est_geral, golpes)

        agent.memoria.ataque_alvo_indice = golpe_escolhido["indice"]
        agent.registrar_acao(est_especifico, est_geral, golpe_escolhido["id"])

    alvo_indice = agent.memoria.ataque_alvo_indice

    if cursor_atual == alvo_indice:
        print(f"🎯 Cursor posicionado no slot {alvo_indice}! Disparando ESPAÇO!")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESPACO.value)

    tecla_mov = tecla_para_alvo(cursor_atual, alvo_indice)
    print(f"🧭 Movendo o cursor do slot {cursor_atual} para {alvo_indice}...")
    return acao(tecla_mov)
