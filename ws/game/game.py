import chess
import json
from channels.generic.websocket import WebsocketConsumer


class Player():
    def __init__(self, channel_name, name):
        self.name = name
        self.channel_name = channel_name

    def __str__(self):
        return f"name: {self.name}, channel name: {self.channel_name}"

class Game():
    def __init__(self, player1: WebsocketConsumer, player2: WebsocketConsumer):
        self.player1 = player1
        self.player2 = player2
        self.board = chess.Board()
        self.moves = []


        # send message to both players with their colors
        self.player1.send(json.dumps({
            "message": "Game Initialized",
            "color": "white"
        }))
        self.player2.send(json.dumps({
            "message": "Game Initialized",
            "color": "black"
        }))

