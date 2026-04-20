from enum import Enum


class Tecla(Enum):
    # Setas direcionais
    ESQUERDA = 37
    CIMA = 38
    DIREITA = 39
    BAIXO = 40

    # Ações principais
    ENTER = 13
    ESPACO = 32
    BACKSPACE = 8
    ESC = 27

    # Letras (muito usadas em emuladores/jogos web)
    Z = 90  # Geralmente Ação / Confirmar
    X = 88  # Geralmente Cancelar / Voltar
    C = 67  # Status / Menu
    R = 82  # Cycle Shiny
    V = 86  # Cycle Tera
