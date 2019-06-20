# # chat/consumers.py
# from channels.generic.websocket import WebsocketConsumer
# import json

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))

# send in 2 second interval
# import asyncio
# from channels.consumer import AsyncConsumer 

# class ChatConsumer(AsyncConsumer):

#     async def websocket_connect(self, event):
#         print("connected", event)
#         print(self.channel_layer)
#         await self.send({
#             "type": "websocket.accept"
#         })

#         while True:
#             await asyncio.sleep(2)

#             # print()
#             obj = "somethign is here"# do_something (Ex: constantly query DB...)

#             await self.send({
#                 'type': 'websocket.send',
#                 'text':     obj,
#             })

#     async def websocket_receive(self, event):
#         print("receive*************************", event)
#         print(json.loads(event))

#     async def websocket_disconnect(self, event):
#         print("disconnected", event)

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.scope["session"]["seed"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # self.scope["session"]["seed"] = random.randint(1, 1000)
        message = text_data_json['message']
        # self.scope["session"]["seed"] = "something"
        # self.scope["session"].save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message + self.scope["session"]["seed"]
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))