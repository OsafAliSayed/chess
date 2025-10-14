import json
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
from game.game import Game, Player

class GameConsumer(WebsocketConsumer):

    pending_user = None
    games = []

    def connect(self):
        # get the name
        query_params = parse_qs(self.scope["query_string"].decode())
        name = query_params.get("name", [None])[0]

        # close connection if name is not given
        if not name:
            self.close(code=6969, reason="name not provided")
            return

        self.accept()

        if not GameConsumer.pending_user:
            GameConsumer.pending_user = self
            self.send(json.dumps({
                "message": "Connection established! waiting for another player!"
            }))
        else:
            game = Game(GameConsumer.pending_user, self)
            GameConsumer.pending_user = None
        

    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "close_connection":
            self.disconnect