"""Agente de Q-Learning: gerencia a Q-Table, hiperparâmetros e memória de batalha."""
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemoriaBatalha:
    """Estado de curto prazo da batalha atual."""
    estado_atual: Optional[str] = None
    estado_anterior: Optional[str] = None
    acao_anterior: Optional[int] = None
    meu_hp_anterior: Optional[int] = None
    inimigo_hp_anterior: Optional[int] = None
    ataque_alvo: Optional[int] = None


class Agent:
    """Cérebro da IA: decide ações e aprende com recompensas via Q-Learning."""

    def __init__(
        self,
        epsilon: float = 1.0,
        decaimento_eps: float = 0.995,
        taxa_aprendizado: float = 0.1,
    ) -> None:
        self.epsilon = epsilon
        self.decaimento_eps = decaimento_eps
        self.taxa_aprendizado = taxa_aprendizado
        self.tabela_q: dict[str, dict[int, float]] = {}
        self.memoria = MemoriaBatalha()

    def escolher_ataque(self, estado: str, qtd_ataques: int) -> int:
        """Política epsilon-greedy: explora aleatoriamente ou explota o melhor ataque conhecido."""
        acoes = self.tabela_q.get(estado)
        deve_explorar = (
            random.random() < self.epsilon
            or not acoes
        )
        if deve_explorar:
            escolha = random.randint(0, qtd_ataques - 1)
            print(f"🎲 [EXPLORAÇÃO] Ataque Slot {escolha} escolhido aleatoriamente.")
        else:
            escolha = max(acoes, key=acoes.get)  # type: ignore[arg-type]
            print(f"🧠 [EXPLOTAÇÃO] Slot {escolha} é o melhor para este estado.")

        self.epsilon = max(0.1, self.epsilon * self.decaimento_eps)
        return escolha

    def registrar_acao(self, estado: str, acao: int) -> None:
        """Salva o estado e ação atuais para receber feedback no próximo turno."""
        self.memoria.estado_anterior = estado
        self.memoria.acao_anterior = acao

    def atualizar_q(
        self,
        estado: str,
        acao: int,
        recompensa: float,
    ) -> None:
        """Aplica a fórmula de Q-Learning para atualizar o valor da ação."""
        self.tabela_q.setdefault(estado, {}).setdefault(acao, 0.0)
        valor_antigo = self.tabela_q[estado][acao]
        self.tabela_q[estado][acao] = (
            valor_antigo + self.taxa_aprendizado * (recompensa - valor_antigo)
        )
        print("-" * 50)
        print(f"📊 [FEEDBACK] Recompensa: {recompensa} | Estado: {estado} | Ação: {acao}")
        print(f"📈 [TABELA Q] Novo valor: {self.tabela_q[estado][acao]:.2f}")
        print("-" * 50)
