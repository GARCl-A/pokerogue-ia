"""Handler inteligente para a tela de confirmação (CONFIRM)."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_confirm(dados: dict, agent) -> dict | None:
    opcoes = dados.get("opcoes", [])
    mensagem = dados.get("mensagem", "").lower()
    cursor_atual = dados.get("cursor", 0)

    print(f"❓ CONFIRM: '{mensagem}' | Opções: {opcoes}")

    # CONFIGURAÇÃO DE ALVO PADRÃO: Aceitar (geralmente índice 0 é 'Sim')
    alvo = 0

    # 🧠 CASO 1: Menu de substituição pós-vitória (4 opções)
    # Segundo o ConfirmUiHandler.ts, essa tela tem 4 opções fixas.
    if len(opcoes) == 4:
        print(
            "🛑 Menu de troca (4 opções) detectado. Recusando para evitar o loop da Party."
        )
        alvo = 3  # Índice do 'Não' no menu: [Summary, Pokedex, Yes, No]

    # 🧠 CASO 2: Pergunta de troca binária (Sim/Não)
    # Aqui usamos a mensagem que você pescou via console!
    elif any(
        termo in mensagem for termo in ["trocar", "switch", "substituir", "change"]
    ):
        for i, texto in enumerate(opcoes):
            t_upper = str(texto).upper()
            if "NÃO" in t_upper or "NAO" in t_upper or "NO" in t_upper:
                alvo = i
                print(f"🛑 Mensagem de troca detectada. Recusando no alvo: {texto}")
                break

    # 🧠 CASO 3: Início de jogo, Evoluções, etc.
    else:
        for i, texto in enumerate(opcoes):
            t_upper = str(texto).upper()
            if "SIM" in t_upper or "YES" in t_upper:
                alvo = i
                print(f"✅ Contexto seguro detectado. Confirmando ação!")
                break

    # Execução da movimentação até o alvo
    if cursor_atual == alvo:
        print(f"🎯 Confirmando opção {alvo} ('{opcoes[alvo]}')")
        return acao(Tecla.ESPACO.value)

    if cursor_atual < alvo:
        return acao(Tecla.BAIXO.value)
    else:
        return acao(Tecla.CIMA.value)
