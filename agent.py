"""Agente de Q-Learning: gere as Q-Tables (Específica e Geral), persistência e memória."""

import random
import json
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoriaBatalha:
    """Estado de curto prazo da batalha atual, com dupla camada."""

    estado_especifico_atual: Optional[str] = None
    estado_geral_atual: Optional[str] = None

    estado_especifico_anterior: Optional[str] = None
    estado_geral_anterior: Optional[str] = None

    acao_anterior: Optional[str] = None
    meu_hp_anterior: Optional[int] = None
    inimigo_hp_anterior: Optional[int] = None
    ataque_alvo_indice: Optional[int] = None


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

        # Separamos os ficheiros!
        self.arquivo_q_esp = "tabela_q.json"  # O seu ficheiro antigo continua aqui
        self.arquivo_q_geral = "tabela_q_tipos.json"  # O novo ficheiro de instintos

        self.memoria = MemoriaBatalha()

        self.tabela_especifica = {}
        self.tabela_geral = {}
        self.carregar_q()

    def carregar_q(self):
        """Carrega as duas memórias de ficheiros separados."""
        if os.path.exists(self.arquivo_q_esp):
            with open(self.arquivo_q_esp, "r") as f:
                self.tabela_especifica = json.load(f)

        if os.path.exists(self.arquivo_q_geral):
            with open(self.arquivo_q_geral, "r") as f:
                self.tabela_geral = json.load(f)

        print(
            f"💾 Cérebro Duplo carregado: {len(self.tabela_especifica)} memórias exatas e {len(self.tabela_geral)} instintos de tipo."
        )

    def salvar_q(self):
        """Guarda as duas tabelas nos seus respetivos ficheiros."""
        with open(self.arquivo_q_esp, "w") as f:
            json.dump(self.tabela_especifica, f, indent=4)
        with open(self.arquivo_q_geral, "w") as f:
            json.dump(self.tabela_geral, f, indent=4)

    def escolher_ataque(
        self, est_especifico: str, est_geral: str, golpes: list[dict]
    ) -> dict:
        """Tenta a Memória Específica, faz Fallback para os Tipos, ou Explora."""
        ids_disponiveis = [str(g["id"]) for g in golpes]

        acoes_esp = self.tabela_especifica.get(est_especifico, {})
        acoes_validas_esp = {k: v for k, v in acoes_esp.items() if k in ids_disponiveis}

        acoes_ger = self.tabela_geral.get(est_geral, {})
        acoes_validas_ger = {k: v for k, v in acoes_ger.items() if k in ids_disponiveis}

        deve_explorar = random.random() < self.epsilon

        if deve_explorar or (not acoes_validas_esp and not acoes_validas_ger):
            escolha = random.choice(golpes)
            print(f"🎲 [EXPLORAÇÃO] Testando Golpe ID {escolha['id']}.")

        elif acoes_validas_esp:
            melhor_id = max(acoes_validas_esp, key=acoes_validas_esp.get)  # type: ignore
            escolha = next(g for g in golpes if str(g["id"]) == melhor_id)
            print(
                f"🧠 [MEMÓRIA EXATA] Eu conheço este bicho! A usar ID {escolha['id']}."
            )

        else:
            melhor_id = max(acoes_validas_ger, key=acoes_validas_ger.get)  # type: ignore
            escolha = next(g for g in golpes if str(g["id"]) == melhor_id)
            print(
                f"🧬 [INSTINTO DE TIPO] Bicho novo, mas conheço os Tipos. A usar ID {escolha['id']}!"
            )

        self.epsilon = max(0.1, self.epsilon * self.decaimento_eps)
        return escolha

    def registrar_acao(self, est_especifico: str, est_geral: str, move_id: int) -> None:
        self.memoria.estado_especifico_anterior = est_especifico
        self.memoria.estado_geral_anterior = est_geral
        self.memoria.acao_anterior = str(move_id)

    def atualizar_q(
        self, est_especifico: str, est_geral: str, acao_id: str, recompensa: float
    ) -> None:
        """Atualiza a nota da ação NAS DUAS tabelas ao mesmo tempo."""
        self.tabela_especifica.setdefault(est_especifico, {}).setdefault(acao_id, 0.0)
        v_antigo_esp = self.tabela_especifica[est_especifico][acao_id]
        self.tabela_especifica[est_especifico][acao_id] = (
            v_antigo_esp + self.taxa_aprendizado * (recompensa - v_antigo_esp)
        )

        self.tabela_geral.setdefault(est_geral, {}).setdefault(acao_id, 0.0)
        v_antigo_ger = self.tabela_geral[est_geral][acao_id]
        self.tabela_geral[est_geral][acao_id] = v_antigo_ger + self.taxa_aprendizado * (
            recompensa - v_antigo_ger
        )

        print("-" * 50)
        print(f"📊 [FEEDBACK DUPLO] Recompensa: {recompensa} | Golpe: {acao_id}")
        print(
            f"   => Específico ({est_especifico}): {self.tabela_especifica[est_especifico][acao_id]:.2f}"
        )
        print(
            f"   => Instinto   ({est_geral}): {self.tabela_geral[est_geral][acao_id]:.2f}"
        )
        print("-" * 50)

        self.salvar_q()
