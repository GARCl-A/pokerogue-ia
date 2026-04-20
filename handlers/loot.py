"""Handler para a tela de recompensas pós-batalha (MODIFIER_SELECT)."""
import importlib
from utils import acao

Tecla = importlib.import_module("teclas").Tecla


def handle_loot(dados: dict, agent) -> dict | None:
    """Escolhe a primeira recompensa disponível com ESPAÇO."""
    recompensas = dados.get("recompensas", [])
    nomes = [r["nome"] for r in recompensas]
    print(f"🎁 Tela de Loot! Recompensas: {nomes}")

    if recompensas:
        print(f"👉 Escolhendo a primeira recompensa ({nomes[0]}) com ESPAÇO!")
        return acao(Tecla.ESPACO.value)

    return None
