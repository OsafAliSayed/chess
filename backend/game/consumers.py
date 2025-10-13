import json
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        print("Whatiz i am in connect")
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'Whatiz'
        }))
    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        pass