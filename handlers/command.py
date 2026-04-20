"""Handler para a tela de comando de batalha (COMMAND): atualiza a Q-Table com a recompensa."""
import importlib
from agent import Agent
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def _formatar_time(time: list[dict]) -> str:
    return " & ".join(f"{p['nome']} (HP: {p['hp']}/{p['hpMax']})" for p in time)


def handle_command(dados: dict, agent: Agent) -> dict:
    """Calcula a recompensa do turno anterior, atualiza a Q-Table e avança para FIGHT."""
    meu_time = dados.get("meuTime", [])
    inimigos = dados.get("inimigos", [])

    if meu_time and inimigos:
        meu_poke = meu_time[0]
        inimigo = inimigos[0]
        hp_atual_meu = meu_poke["hp"]
        hp_atual_inimigo = inimigo["hp"]

        estado_atual = f"{meu_poke['nome']}_vs_{inimigo['nome']}"
        agent.memoria.estado_atual = estado_atual

        # Calcula recompensa e atualiza Q-Table se houver ação anterior registrada
        if agent.memoria.acao_anterior is not None:
            dano_causado = max(0, (agent.memoria.inimigo_hp_anterior or 0) - hp_atual_inimigo)
            dano_sofrido = max(0, (agent.memoria.meu_hp_anterior or 0) - hp_atual_meu)
            recompensa = dano_causado - dano_sofrido
            agent.atualizar_q(
                agent.memoria.estado_anterior,  # type: ignore[arg-type]
                agent.memoria.acao_anterior,
                recompensa,
            )

        agent.memoria.meu_hp_anterior = hp_atual_meu
        agent.memoria.inimigo_hp_anterior = hp_atual_inimigo

        print(f"⚔️ BATALHA! [{_formatar_time(meu_time)}] VS [{_formatar_time(inimigos)}]")

    return acao(Tecla.ESPACO.value)
