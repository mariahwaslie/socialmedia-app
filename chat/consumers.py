import json
from django.http import JsonResponse
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message, SingleChat, ChatRoom
from django.db.models import Q
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from notifications.signals import notify



User = get_user_model()
class SingleChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.single_chat = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'single_chat_{self.single_chat}'
        self.user = self.scope['user']


#         # Join chat room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

#         # Accept the WebSocket connection
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
#
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_body = text_data_json['message']
        sender = self.scope['user']
#
        # Save the message to the database
        chat = await sync_to_async(SingleChat.objects.get)(id=self.single_chat)
        recipients = await sync_to_async(lambda: chat.participants.exclude(id=sender.id).first())()
        message = await sync_to_async(SingleChat.send_message)(chat, sender, recipients, message_body)

        # Send notification to the recipient
        await sync_to_async(notify.send)(
            sender,
            recipient=recipients,
            verb=f'{sender} sent you a message',
            description=message_body,
            target=chat
        )

        # Broadcast the new message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_body,
                'sender': sender.username,
            }
        )
#
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
#
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'sender': sender,
        }))




class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group= self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_room_{self.room_group}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
#
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
#
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_body = text_data_json['message']
        sender = self.scope['user']

        # Save the message to the database
        chat_room = await sync_to_async(ChatRoom.objects.get)(id=self.room_group)
        participants = await sync_to_async(lambda: chat_room.participants.all())()
        await sync_to_async(ChatRoom.send_message)(chat_room, sender, participants, message_body)

        # Send notification to all participants except the sender
        for participant in participants:
            if participant != sender:
                await sync_to_async(notify.send)(
                    sender,
                    recipient=participant,
                    verb=f'{sender.username} sent a message in {chat_room.name}',
                    description=message_body,
                    target=chat_room
                )

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_body,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
