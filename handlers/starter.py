"""Handler para a tela de seleção de Pokémon inicial (STARTER_SELECT)."""
import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_starter_select(dados: dict, agent) -> dict:
    """Seleciona Pokémons iniciais até o custo do time atingir o limite, depois inicia."""
    pokemon = dados.get("pokemonNoCursor", "Vazio")
    custo_time = dados.get("custoAtual", 0)
    pode_comecar = dados.get("podeComecar", False)
    print(f"🤔 IA Pensando: Estou olhando para o {pokemon}. Custo do time: {custo_time}/10")

    if pode_comecar:
        print("✅ O time está válido! Vou apertar MENU/START para começar o jogo.")
        return acao(Tecla.ESC.value)

    if pokemon != "Vazio" and custo_time < 10:
        print(f"👉 Apertando ESPAÇO para tentar pegar o {pokemon}!")
        return acao(Tecla.ESPACO.value)

    print("➡️ Movendo pra direita...")
    return acao(Tecla.DIREITA.value)
