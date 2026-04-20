"""Handler para a tela de seleção de ataque (FIGHT)."""
import importlib
from agent import Agent
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla


def handle_fight(dados: dict, agent: Agent) -> dict | None:
    """Decide qual ataque usar (Q-Learning) e navega o cursor até ele."""
    qtd_ataques = dados.get("quantidadeAtaques", 0)
    cursor_atual = dados.get("cursor", 0)
    estado_atual = agent.memoria.estado_atual or "Desconhecido"

    if qtd_ataques == 0:
        return None

    # 1. CÉREBRO PENSA — só decide se não houver alvo travado
    if agent.memoria.ataque_alvo is None:
        ataque_escolhido = agent.escolher_ataque(estado_atual, qtd_ataques)
        agent.memoria.ataque_alvo = ataque_escolhido
        agent.registrar_acao(estado_atual, ataque_escolhido)

    # 2. MÃOS EXECUTAM — navega o cursor até o alvo
    alvo = agent.memoria.ataque_alvo
    if cursor_atual == alvo:
        print(f"🎯 Cursor no alvo ({alvo})! Disparando ESPAÇO!")
        agent.memoria.ataque_alvo = None
        return acao(Tecla.ESPACO.value)

    tecla_mov = tecla_para_alvo(cursor_atual, alvo)
    print(f"🧭 Movendo o cursor de {cursor_atual} para {alvo}...")
    return acao(tecla_mov)
