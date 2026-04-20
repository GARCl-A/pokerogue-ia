"""Handlers para as telas de equipe (PARTY) e seleção de alvo (TARGET_SELECT)."""

import importlib
from utils import acao, tecla_para_alvo

Tecla = importlib.import_module("teclas").Tecla


def handle_party(dados: dict, agent) -> dict:
    time = dados.get("time", [])
    cursor_atual = dados.get("cursor", 0)
    mensagem = dados.get("mensagem", "").lower()

    # Identifica o contexto da ação
    is_tm = "ensina" in mensagem or "teach" in mensagem
    is_revive = "reanima" in mensagem or "revive" in mensagem
    is_usando_item = any(
        t in mensagem
        for t in [
            "escolha",
            "ensina",
            "aumenta",
            "reanima",
            "restaura",
            "choose",
            "teach",
            "cura",
        ]
    )

    if not time:
        return acao(Tecla.X.value)

    # 1. CÉREBRO: Decide o alvo
    if agent.memoria.ataque_alvo_indice is None:

        # Trava de Segurança para não fechar a tela de item achando que é troca de batalha
        lead_vivo = time[0].get("hp", 0) > 0
        if not is_usando_item and lead_vivo:
            print(
                f"🚫 Líder ({time[0]['nome']}) está vivo e não há contexto de item. Saindo..."
            )
            return acao(Tecla.X.value)

        alvo = None

        for i, p in enumerate(time):
            hp = p.get("hp", 0)
            aptidao = p.get("aptidao", "").lower()  # <--- Lendo a UI do jogo!

            # CASO 1: Ensinando um TM
            if is_tm:
                # Se na tela estiver escrito que ele não pode ou já aprendeu, ignora.
                # Adapte as palavras de acordo com a linguagem que você joga (Inglês ou PT)
                if any(
                    erro in aptidao
                    for erro in [
                        "incapaz",
                        "não pode",
                        "not able",
                        "aprendido",
                        "learned",
                    ]
                ):
                    print(
                        f"⏭️ {p['nome']} ignorado (Incompatível ou já sabe o golpe: '{aptidao}')"
                    )
                    continue

                # Se for Capaz, é ele mesmo!
                alvo = i
                break

            # CASO 2: Usando item de Reviver (Precisa estar morto)
            elif is_revive:
                if hp == 0:
                    alvo = i
                    break

            # CASO 3: Troca em batalha ou Cura (Precisa estar vivo)
            else:
                if hp > 0:
                    # Se for poção e o jogo disser que não tem efeito (vida cheia)
                    if is_usando_item and any(
                        erro in aptidao for erro in ["efeito", "effect"]
                    ):
                        continue

                    alvo = i
                    break

        # Se ninguém for alvo válido (ex: pegou um TM de Água e só tem Pokémon de Fogo)
        if alvo is None:
            print("⚠️ Nenhum Pokémon no time pode receber essa ação. Cancelando (X)...")
            return acao(Tecla.X.value)

        agent.memoria.ataque_alvo_indice = alvo

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
