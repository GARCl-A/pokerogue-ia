"""Agente de Q-Learning: gerencia a Q-Table, persistência no disco e memória de batalha."""

import random
import json
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoriaBatalha:
    """Estado de curto prazo da batalha atual."""

    estado_atual: Optional[str] = None
    estado_anterior: Optional[str] = None
    acao_anterior: Optional[str] = (
        None  # Mudou para String para compatibilidade com chaves JSON (Move ID)
    )
    meu_hp_anterior: Optional[int] = None
    inimigo_hp_anterior: Optional[int] = None
    ataque_alvo_indice: Optional[int] = (
        None  # O índice físico para onde o cursor deve ir
    )


class Agent:
    def __init__(
        self,
        epsilon: float = 1.0,
        decaimento_eps: float = 0.995,
        taxa_aprendizado: float = 0.1,
    ) -> None:
        self.epsilon = epsilon
        self.decaimento_eps = decaimento_eps
        self.taxa_aprendizado = taxa_aprendizado
        self.arquivo_q = "tabela_q.json"
        self.memoria = MemoriaBatalha()
        self.carregar_q()

    def carregar_q(self):
        """Carrega a memória de longo prazo do disco."""
        if os.path.exists(self.arquivo_q):
            with open(self.arquivo_q, "r") as f:
                self.tabela_q = json.load(f)
            print(
                f"💾 Memória carregada com sucesso! ({len(self.tabela_q)} lutas conhecidas)"
            )
        else:
            self.tabela_q = {}
            print("🧠 Nova Tabela Q criada. O bot não tem memórias anteriores.")

    def salvar_q(self):
        """Salva a memória no disco para não esquecer ao desligar."""
        with open(self.arquivo_q, "w") as f:
            json.dump(self.tabela_q, f, indent=4)

    def escolher_ataque(self, estado: str, golpes: list[dict]) -> dict:
        """Pensa com base no Move ID, não na posição física."""
        acoes_conhecidas = self.tabela_q.get(estado, {})
        deve_explorar = random.random() < self.epsilon or not acoes_conhecidas

        if deve_explorar:
            escolha = random.choice(golpes)
            print(f"🎲 [EXPLORAÇÃO] Golpe ID {escolha['id']} escolhido aleatoriamente.")
        else:
            # Filtra a tabela Q apenas para os golpes que o Pokémon possui NESTE MOMENTO
            ids_disponiveis = [str(g["id"]) for g in golpes]
            acoes_validas = {
                k: v for k, v in acoes_conhecidas.items() if k in ids_disponiveis
            }

            if acoes_validas:
                # Pega o ID do ataque com maior pontuação
                melhor_id_str = max(acoes_validas, key=acoes_validas.get)
                # Encontra as coordenadas dele na lista atual enviada pelo jogo
                escolha = next(g for g in golpes if str(g["id"]) == melhor_id_str)
                print(
                    f"🧠 [EXPLOTAÇÃO] Golpe ID {escolha['id']} é o melhor para este inimigo!"
                )
            else:
                # Conhece o inimigo, mas não tem nenhum dos golpes antigos que funcionavam. Explora!
                escolha = random.choice(golpes)
                print(
                    f"🎲 [EXPLORAÇÃO FORÇADA] Golpes novos na build! Testando ID {escolha['id']}."
                )

        self.epsilon = max(0.1, self.epsilon * self.decaimento_eps)
        return escolha

    def registrar_acao(self, estado: str, move_id: int) -> None:
        """Salva o ID do golpe na memória curta para dar nota no fim do turno."""
        self.memoria.estado_anterior = estado
        self.memoria.acao_anterior = str(
            move_id
        )  # IDs viram strings para salvar no JSON

    def atualizar_q(self, estado: str, acao_id: str, recompensa: float) -> None:
        """Atualiza a nota do golpe e grava no HD."""
        self.tabela_q.setdefault(estado, {}).setdefault(acao_id, 0.0)
        valor_antigo = self.tabela_q[estado][acao_id]

        # A Mágica de Bellman
        self.tabela_q[estado][acao_id] = valor_antigo + self.taxa_aprendizado * (
            recompensa - valor_antigo
        )

        print("-" * 50)
        print(
            f"📊 [FEEDBACK] Recompensa: {recompensa} | Estado: {estado} | Golpe ID: {acao_id}"
        )
        print(f"📈 [TABELA Q] Novo valor: {self.tabela_q[estado][acao_id]:.2f}")
        print("-" * 50)

        self.salvar_q()  # Imprime a memória no HD
