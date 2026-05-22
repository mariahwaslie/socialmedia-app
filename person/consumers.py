from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import logging
from .models import Post, Comments


logger = logging.getLogger(__name__)

# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This method is called when the WebSocket is handshaking as part of connection process.
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"upload_{self.room_name}"

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
        data = json.loads(text_data)
        message = data.get('message')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video_upload_status',
                'message': message
            }
        )

    # Receive message from room group
    async def video_upload_status(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'notifications',
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'notifications',
            self.channel_name
        )
        raise StopConsumer()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            'notifications',
            {
                'type': 'send_notification',
                'message': data['message']
            }
        )
        pass

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'comments_{self.id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # comment = text_data_json['comment']
        # profile_picture = self.scope['user_profile_picture']
        # username = self.scope['username']
        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'comment_message',
        #         'comment': comment,
        #         'profile_picture': profile_picture,
        #         'username': username
        #     }
        # )

    # Receive message from room group
    async def comment_message(self, event):
        comment = event['comment']
        profile_picture = event['profile_picture']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment,
            'profile_picture': profile_picture,
            'username': username
        }))