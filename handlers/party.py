"""Handlers para as telas de equipe (PARTY) e seleção de alvo (TARGET_SELECT)."""

import importlib
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla


def handle_party(dados: dict, agent) -> dict:
    time = dados.get("time", [])
    cursor_atual = dados.get("cursor", 0)
    mensagem = dados.get("mensagem", "").lower()

    # Contextos de uso de item ou ensino de golpe
    is_usando_item = any(t in mensagem for t in ["escolha", "ensina"])

    if not time:
        return acao(Tecla.X.value)

    # 1. CÉREBRO: Decide o alvo
    if agent.memoria.ataque_alvo_indice is None:
        # --- CORREÇÃO DA TRAVA DE SEGURANÇA ---
        # O líder (Slot 0) é quem define se a tela de troca forçada é legítima
        lead_vivo = time[0].get("hp", 0) > 0

        if not is_usando_item and lead_vivo:
            print(
                f"🚫 Líder ({time[0]['nome']}) está vivo e não há contexto de item. Saindo..."
            )
            return acao(Tecla.X.value)
        # ---------------------------------------

        alvo = None
        # Se chegamos aqui, ou o líder morreu ou estamos usando um item.
        # Procuramos o primeiro Pokémon com vida para entrar em campo ou receber o item.
        for i, p in enumerate(time):
            if p.get("hp", 0) > 0:
                # Se for item e já tentamos o primeiro (e falhou), tentamos o próximo
                if is_usando_item and "não pode aprender" in mensagem:
                    if i <= cursor_atual:
                        continue

                alvo = i
                break

        agent.memoria.ataque_alvo_indice = alvo if alvo is not None else 0

    # 2. MÃOS: Navega e confirma
    alvo_indice = agent.memoria.ataque_alvo_indice

    if cursor_atual == alvo_indice:
        nome_alvo = time[alvo_indice].get("nome", "Desconhecido")
        print(f"👉 Selecionando {nome_alvo} (Slot {alvo_indice})!")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESPACO.value)

    tecla_mov = tecla_para_alvo(cursor_atual, alvo_indice)
    print(f"🧭 Movendo cursor na equipe (Slot {cursor_atual} -> {alvo_indice})...")
    return acao(tecla_mov)


def handle_target_select(dados: dict, agent) -> dict:
    print("🎯 Batalha em Dupla! Selecionando alvo com ESPAÇO...")
    return acao(Tecla.ESPACO.value)
