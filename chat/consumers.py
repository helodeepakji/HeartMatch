# chat/consumers.py
import json
from chat.models import Chat
import datetime
from django.contrib.auth import authenticate
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.scope['user'].is_authenticated:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            room_name = self.scope['url_route']['kwargs']['room_name']
            user = str(self.scope['user'])
            if(message == "videocall by "+room_name):
                print("videocall by "+user)
                n = len(str(user))
                print(n)
                print(room_name)

                touser = room_name[:-n]
                exuser = room_name[n:]

                print(touser)
                print(exuser)

                if str(user) == str(room_name[len(touser):]):
                    exuser = str(room_name[len(touser):])
                    touser = str(room_name[:-len(user)])
                    print(touser)
                    print(exuser)

                if str(user) == str(room_name[:-len(touser)]):
                    exuser = str(room_name[:-len(touser)])
                    touser = str(room_name[len(user):])
                    print(touser)
                    print(exuser)

                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat_message",
                                        "message": touser, "user": user}
                )
            else:
                chat = Chat(username=user, chat=message,
                            room=room_name, datetime=datetime.datetime.now())
                await sync_to_async(chat.save)()
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "chat_message", "message": message, "user": user}
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user": user}))
