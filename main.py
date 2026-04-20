"""Ponto de entrada: sobe o servidor WebSocket e orquestra as mensagens recebidas do jogo."""

import asyncio
import importlib
import json

import websockets

from agent import Agent
from router import rotear

UiMode = importlib.import_module("ui-mode").UiMode


async def ponte_pokerogue(websocket) -> None:
    """Gerencia uma conexão com o jogo: decodifica mensagens e despacha para o roteador."""
    agent = Agent()
    print("🎮 Jogo conectado com sucesso!")
    try:
        async for mensagem_bruta in websocket:
            try:
                mensagem = json.loads(mensagem_bruta)
                if mensagem.get("tipo") != "ESTADO_DO_JOGO":
                    continue

                numero_tela = int(mensagem["tela"])
                try:
                    nome_tela = UiMode(numero_tela).name
                except ValueError:
                    nome_tela = f"TELA_NAO_MAPEADA ({numero_tela})"

                print(f"👀 A IA está vendo a tela: {nome_tela}")

                dados = mensagem.get("dados", {})
                resposta = rotear(nome_tela, dados, agent)
                if resposta is not None:
                    await websocket.send(json.dumps(resposta))

            except json.JSONDecodeError:
                print(f"💬 Mensagem de texto: {mensagem_bruta}")

    except websockets.exceptions.ConnectionClosed:
        print("❌ O jogo desconectou.")


async def main() -> None:
    async with websockets.serve(ponte_pokerogue, "localhost", 8765):
        print("📡 Servidor da IA rodando em ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
