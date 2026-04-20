"""Handler para a tela de seleção de ataque (FIGHT)."""

import importlib
from agent import Agent
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla
PokemonTypes = importlib.import_module("tipos_pokemon").PokemonTypes


def _nome_tipo(id_tipo: int) -> str:
    """Traduz o ID numérico do tipo para texto usando o Enum."""
    try:
        return str(PokemonTypes(id_tipo))
    except ValueError:
        return f"Tipo_{id_tipo}"


def handle_fight(dados: dict, agent: Agent) -> dict | None:
    golpes = dados.get("golpes", [])
    cursor_atual = dados.get("cursor", 0)
    nome_ativo = dados.get("nomeAtivo")
    inimigos = dados.get("inimigos", [])
    ativo_index = dados.get("ativoIndex", 0)  # <--- PEGANDO O SLOT DO TS

    if not golpes:
        return None

    # 1. SINCRONIZAÇÃO EM TEMPO REAL E MIRA INTELIGENTE
    if nome_ativo and inimigos:
        # A Regra da Mira em Duplas:
        # Se eu sou o Slot 0, avalio o Inimigo do Slot 0.
        # Se eu sou o Slot 1, avalio o Inimigo do Slot 1.
        if len(inimigos) > ativo_index:
            inimigo = inimigos[ativo_index]
        else:
            inimigo = inimigos[0]  # Fallback caso o inimigo da frente já tenha morrido

        # Atualiza Memória Específica com o alvo real
        est_especifico = f"{nome_ativo}_vs_{inimigo['nome']}"

        # Atualiza Instinto (Geral)
        tipo1 = inimigo.get("tipo1", -1)
        tipo2 = inimigo.get("tipo2", tipo1)
        nome_t1 = _nome_tipo(tipo1)
        nome_t2 = _nome_tipo(tipo2)

        if nome_t1 == nome_t2:
            est_geral = f"Inimigo_{nome_t1}"
        else:
            est_geral = f"Inimigo_{nome_t1}-{nome_t2}"

        agent.memoria.estado_especifico_atual = est_especifico
        agent.memoria.estado_geral_atual = est_geral
    else:
        est_especifico = agent.memoria.estado_especifico_atual or "Desconhecido"
        est_geral = agent.memoria.estado_geral_atual or "T_Desconhecido"

    # 2. ESCOLHA DE GOLPE
    if agent.memoria.ataque_alvo_indice is None:
        golpe_escolhido = agent.escolher_ataque(est_especifico, est_geral, golpes)

        agent.memoria.ataque_alvo_indice = golpe_escolhido["indice"]
        agent.registrar_acao(est_especifico, est_geral, golpe_escolhido["id"])

    alvo_indice = agent.memoria.ataque_alvo_indice

    # 3. TRAVA ANTI-LOOP
    indices_validos = [g["indice"] for g in golpes]
    if alvo_indice not in indices_validos:
        print(f"⚠️ Alvo {alvo_indice} inválido (slot vazio). Resetando escolha...")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESQUERDA.value)

    # 4. EXECUÇÃO
    if cursor_atual == alvo_indice:
        print(f"🎯 Cursor no slot {alvo_indice} contra {est_especifico}! Disparando.")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESPACO.value)

    tecla_mov = tecla_para_alvo(cursor_atual, alvo_indice)
    print(f"🧭 Movendo o cursor do slot {cursor_atual} para {alvo_indice}...")
    return acao(tecla_mov)
