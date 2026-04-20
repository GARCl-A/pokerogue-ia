"""Handler para a tela de comando de batalha (COMMAND): atualiza a Q-Table com a recompensa."""

import importlib
from agent import Agent
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def _formatar_time(time: list[dict]) -> str:
    return " & ".join(f"{p['nome']} (HP: {p['hp']}/{p['hpMax']})" for p in time)


def handle_command(dados: dict, agent: Agent) -> dict:
    meu_time = dados.get("meuTime", [])
    inimigos = dados.get("inimigos", [])

    if meu_time and inimigos:
        meu_poke = meu_time[0]
        inimigo = inimigos[0]
        hp_atual_meu = meu_poke["hp"]
        hp_atual_inimigo = inimigo["hp"]

        # 1. Memória Fotográfica (O original)
        estado_especifico = f"{meu_poke['nome']}_vs_{inimigo['nome']}"

        # 2. Instinto focado no Inimigo (A nova abstração)
        tipo1 = inimigo.get("tipo1", 0)
        tipo2 = inimigo.get("tipo2", 0)
        estado_geral = f"InimigoT_{tipo1}-{tipo2}"

        agent.memoria.estado_especifico_atual = estado_especifico
        agent.memoria.estado_geral_atual = estado_geral

        if agent.memoria.acao_anterior is not None:
            dano_causado = max(
                0, (agent.memoria.inimigo_hp_anterior or 0) - hp_atual_inimigo
            )
            dano_sofrido = max(0, (agent.memoria.meu_hp_anterior or 0) - hp_atual_meu)
            recompensa = dano_causado - dano_sofrido

            agent.atualizar_q(
                agent.memoria.estado_especifico_anterior,  # type: ignore
                agent.memoria.estado_geral_anterior,  # type: ignore
                agent.memoria.acao_anterior,
                recompensa,
            )

        agent.memoria.meu_hp_anterior = hp_atual_meu
        agent.memoria.inimigo_hp_anterior = hp_atual_inimigo

        print(
            f"⚔️ BATALHA! [{_formatar_time(meu_time)}] VS [{_formatar_time(inimigos)}]"
        )

    return acao(Tecla.ESPACO.value)
