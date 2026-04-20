"""Handlers para as telas de equipe (PARTY) e seleção de alvo (TARGET_SELECT)."""
import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_party(dados: dict, agent) -> dict:
    """Seleciona o Pokémon sob o cursor na tela de equipe."""
    time = dados.get("time", [])
    cursor_atual = dados.get("cursor", 0)

    if time and cursor_atual < len(time):
        poke = time[cursor_atual]
        print(f"🎒 Tela de Equipe! Apontando para: {poke['nome']} (HP: {poke['hp']}/{poke['hpMax']})")
    else:
        print("🎒 Tela de Equipe! Lendo os dados...")

    print("👉 Apertando ESPAÇO para selecionar este alvo!")
    return acao(Tecla.ESPACO.value)


def handle_target_select(dados: dict, agent) -> dict:
    """Confirma o alvo em batalhas duplas com ESPAÇO."""
    print("🎯 Batalha em Dupla! Selecionando alvo com ESPAÇO...")
    return acao(Tecla.ESPACO.value)
