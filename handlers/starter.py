"""Handler para a tela de seleção de Pokémon inicial (STARTER_SELECT)."""

import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_starter_select(dados: dict, agent) -> dict:
    """
    Seleciona o Bulbassauro e o Pokémon imediatamente à sua direita.
    Inicia o jogo assim que os dois estiverem no time.
    """
    pokemon = dados.get("pokemonNoCursor", "Vazio")
    custo_time = dados.get("custoAtual", 0)
    pode_comecar = dados.get("podeComecar", False)

    print(f"📋 Seleção de Iniciais: {pokemon} | Custo Atual: {custo_time}/10")

    # Se já selecionamos o Bulbassauro (custo > 0) e o vizinho,
    # e o jogo permite começar, iniciamos a run.
    # Nota: Usamos custo_time > 3 porque o Bulba custa 3, então com o vizinho será maior.
    if pode_comecar and custo_time > 3:
        print("🚀 Time pronto (Bulbassauro + Reforço). Iniciando run!")
        return acao(Tecla.ESC.value)

    # FASE 1: Se o custo é 0, ainda estamos procurando o Bulbassauro.
    if custo_time == 0:
        if pokemon == "Bulbasaur":
            print("🌿 Bulbassauro encontrado! Selecionando...")
            return acao(Tecla.ESPACO.value)
        else:
            print("🔍 Navegando até encontrar o Bulbassauro...")
            return acao(Tecla.DIREITA.value)

    # FASE 2: Bulbassauro já selecionado (custo > 0).
    # Se ainda estivermos em cima dele, precisamos mover para a direita.
    if pokemon == "Bulbasaur":
        print("➡️ Bulbassauro garantido. Movendo para o Pokémon à direita...")
        return acao(Tecla.DIREITA.value)

    # FASE 3: Estamos em cima de qualquer outro Pokémon à direita do Bulbassauro.
    # Vamos selecioná-lo para fechar a dupla inicial.
    print(f"➕ Selecionando {pokemon} para ajudar nas batalhas de dupla!")
    return acao(Tecla.ESPACO.value)
