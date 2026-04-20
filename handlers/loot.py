"""Handler para a tela de recompensas pós-batalha (MODIFIER_SELECT)."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_loot(dados: dict, agent) -> dict | None:
    """Finaliza recompensas pendentes e escolhe o item."""
    recompensas = dados.get("recompensas", [])
    nomes = [r["nome"] for r in recompensas]
    if agent.memoria.acao_anterior is not None:
        dano_causado = agent.memoria.inimigo_hp_anterior or 0
        recompensa_final = dano_causado + 10  # Bônus por KO
        print(
            f"🏆 [VITÓRIA] Finalizando recompensa letal para o golpe {agent.memoria.acao_anterior}"
        )
        agent.atualizar_q(
            agent.memoria.estado_especifico_anterior,
            agent.memoria.estado_geral_anterior,
            agent.memoria.acao_anterior,
            recompensa_final,
        )
        agent.memoria.acao_anterior = None
    print(f"🎁 Tela de Loot! Recompensas: {nomes}")
    if recompensas:
        print(f"👉 Escolhendo a primeira recompensa ({nomes[0]}) com ESPAÇO!")
        return acao(Tecla.ESPACO.value)
    return None
