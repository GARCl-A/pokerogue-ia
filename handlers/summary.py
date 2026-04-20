"""Handler para a tela de status e aprendizado de golpes (SUMMARY)."""

import random
import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_summary(dados: dict, agent) -> dict | None:
    """Se estiver aprendendo um golpe, escolhe aleatoriamente se aprende ou cancela."""
    aprendendo_golpe = dados.get("aprendendoGolpe", False)
    cursor_atual = dados.get("cursor", -1)

    if not aprendendo_golpe:
        # Se abriu a tela sem querer (só olhando status), aperta ESC/X para fechar
        print("ℹ️ Tela de Status aberta. Fechando...")
        return acao(Tecla.X.value)

    golpes_atuais = dados.get("golpesAtuais", [])
    golpe_novo = dados.get("golpeNovo", "Desconhecido")

    # 1. CÉREBRO PENSA: Escolhe uma meta (0 a 3 para esquecer um golpe, 4 para cancelar)
    # AQUI FOI A CORREÇÃO: ataque_alvo mudou para ataque_alvo_indice
    if agent.memoria.ataque_alvo_indice is None:
        escolha = random.randint(0, 4)
        agent.memoria.ataque_alvo_indice = escolha

        if escolha == 4:
            print(f"🧠 [BUILD] O Cérebro decidiu NÃO APRENDER o golpe {golpe_novo}.")
        else:
            print(
                f"🧠 [BUILD] O Cérebro decidiu esquecer o Slot {escolha} para aprender {golpe_novo}."
            )

    alvo = agent.memoria.ataque_alvo_indice

    # 2. MÃOS EXECUTAM: Navegando o menu vertical (0 a 4)
    if cursor_atual == alvo:
        print(f"🎯 Cursor no alvo ({alvo})! Confirmando!")
        agent.memoria.ataque_alvo_indice = None
        return acao(Tecla.ESPACO.value)

    # Navegação vertical simples
    if cursor_atual < alvo:
        print(f"🧭 Descendo o cursor ({cursor_atual} -> {alvo})...")
        return acao(Tecla.BAIXO.value)
    else:
        print(f"🧭 Subindo o cursor ({cursor_atual} -> {alvo})...")
        return acao(Tecla.CIMA.value)
