"""Handler para a tela de recompensas pós-batalha (MODIFIER_SELECT)."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_loot(dados: dict, agent) -> dict | None:
    """Finaliza recompensas pendentes e escolhe o item."""
    recompensas = dados.get("recompensas", [])
    nomes = [r["nome"] for r in recompensas]

    # === CORREÇÃO: CAPTURAR RECOMPENSA DE GOLPE LETAL ===
    if agent.memoria.acao_anterior is not None:
        # Se chegamos no loot, o inimigo morreu (HP = 0)
        # O dano causado é o HP total que o inimigo tinha antes do último golpe
        dano_causado = agent.memoria.inimigo_hp_anterior or 0

        # O dano sofrido seria a diferença de HP do meu pokemon, mas como
        # a tela de loot não envia o HP atual de forma simples, podemos
        # considerar apenas o dano causado como bônus de vitória.
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

        # Limpa a memória para não duplicar no próximo comando
        agent.memoria.acao_anterior = None
    # ===================================================

    print(f"🎁 Tela de Loot! Recompensas: {nomes}")
    if recompensas:
        print(f"👉 Escolhendo a primeira recompensa ({nomes[0]}) com ESPAÇO!")
        return acao(Tecla.ESPACO.value)

    return None
