import json
import chess
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
from game.game import Game, Player

class GameConsumer(WebsocketConsumer):

    pending_user: WebsocketConsumer = None
    games: list[Game] = []

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
            GameConsumer.games.append(game)
            GameConsumer.pending_user = None
        

    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "close_connection":
            self.disconnect

        if data["type"] == "board":
            game = self._get_related_game()
            print(game.board)
        
        if data["type"] == "move":
            
            
            game = self._get_related_game()
            # see if it is this players turn
            if len(game.board.move_stack) % 2 == 0 and game.player2 == self:
                self.send(json.dumps({
                    "message": "It is white's move"
                }))
                return

            if len(game.board.move_stack) % 2 == 1 and game.player1 == self:
                self.send(json.dumps({
                    "message": "It is black's move"
                }))
                return
            
    
            # check if it is already mate
            if game.board.is_game_over():
                game.player1.send(json.dumps({
                    "type": "result",
                    "result": game.board.result()
                }))
            move = chess.Move.from_uci(data["move"])

            # reject illegal move
            if not game.board.is_legal(move):
                self.send(json.dumps({
                    "message": "Invalid move"
                }))
                return
            
            # update the board
            game.board.push(move)

            # send the move to other party

            opposition = game.player2 if self == game.player1 else game.player1

            opposition.send(json.dumps({
                "type": "move",
                "color": "black" if len(game.board.move_stack) % 2 == 0 else "white",
                "move": data["move"]
            }))
            

            

    def _get_related_game(self):
        related_game: Game = None
        for game in GameConsumer.games:
            if game.player1 == self or game.player2 == self:
                related_game = game
                break
        return related_game