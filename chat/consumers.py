from asyncio.windows_events import NULL
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Clients
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from random import choice

class ChatConsumer(WebsocketConsumer) : 
    user_channel_name = NULL
     
    def connect(self):
        if(Clients.objects.count() == 0):
            self.accept()
            Clients.objects.create(channel_name = self.channel_name)
            self.send(json.dumps({
                'type' : 'user.searching'
            }))
        else:
            ids = Clients.objects.values_list('id' , flat=True)
            random_id = choice(ids)
            random_client = Clients.objects.get(id = random_id)
            self.user_channel_name = random_client.channel_name
            print(self.user_channel_name)
            self.accept()
            self.send(json.dumps({
                'type' : 'user.found'
            }))
            async_to_sync(self.channel_layer.send) (self.user_channel_name , {
                'type' : 'user.request' , 
                'user_channel_name' :  self.channel_name,
            })
            # Clients.objects.filter(channel_name = self.user_channel_name).delete()
            print("User request was sent")
        
    def disconnect(self, code):
        print(code)
        if(self.user_channel_name == NULL):
            Clients.objects.filter(channel_name = self.channel_name).delete()
        else:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send) (self.user_channel_name , {
                'type' : 'user.disconnect'
            })

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type_message = text_data_json['type']

        if type_message == "typing":
            self.self_typing()
        elif type_message == "message":
            self.message_send(text_data_json["message"])

    #Helper functions to be called from the recieve function
    def self_typing(self):
        async_to_sync(self.channel_layer.send) (
            self.user_channel_name,
            {
                'type' : 'user.typing'
            }
        )

    def message_send(self , message):
        async_to_sync(self.channel_layer.send) (
            self.user_channel_name ,
            {
            'type' : 'message.recieve',
            'message' : message
        })

    #methods to be called when a message is sent in channel layers

    def user_request(self , event):
        self.user_channel_name = event["user_channel_name"]
        Clients.objects.filter(channel_name = self.channel_name).delete()
        self.send(json.dumps({
            'type' : 'user.found'
        }))

    def user_disconnect(self , event):
        self.send(json.dumps({
            'type' : 'user.disconnected'
        }))
    
    def user_typing(self , event):
        self.send(json.dumps({
            'type' : 'user.typing'
        }))

    def message_recieve(self , event):
        message = event['message']
        self.send(json.dumps({
            'type' : 'message.recieve',
            'message': message
        }))

