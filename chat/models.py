from datetime import timezone
from urllib import request

from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from groups.models import Group,Event



# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user',default=None)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    body = HTMLField()
    date=models.DateTimeField(auto_now_add=True)
    is_read =models.BooleanField(default=False)
    def __str__(self):
        return f'{self.sender} {self.body}'
    @classmethod
    def send_message(cls, sender, recipient,body):
        sender_message= Message(
            user = sender,
            sender = sender,
            recipient = recipient,
            body = body,
            is_read= True,
        )
        sender_message.save()
        recipient_message = Message(
            user=recipient,
            sender=sender,
            recipient=recipient,
            body=body,
            is_read = True,
        )
        recipient_message.save()

    @classmethod
    def get_message(cls, user, from_user):
        return Message.objects.filter(user=user, sender=from_user).order_by('date')
    @classmethod
    def count_unread_messages(cls, user):
        return Message.objects.filter(user=user, is_read=False).count()
class ChatRoom(models.Model):
    name= models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_chatrooms')
    created_at = models.DateTimeField(default=now)
    description= models.TextField(blank=True, max_length=500)
    participants = models.ManyToManyField(User,related_name='chatrooms')
    group_messages = models.ManyToManyField(Message,related_name='group_messages')
    group = models.ForeignKey(Group,on_delete=models.SET_NULL, null=True, related_name='chatrooms')
    # event = models.ForeignKey(Event,on_delete=models.SET_NULL, null=True, related_name='event_chat')
    def __str__(self):
        return self.name
    @classmethod
    def get_messages(cls,name):
        # gets the chatroom with a specific name
        messages = Message.objects.filter(name=name)
        return messages

    @classmethod
    def send_message(cls, chatroom ,sender,participants, body):

        for participant in participants:

            sender_message = Message(
                user=sender,
                sender=sender,
                recipient=participant,
                body=body,
                is_read=True,
            )
            sender_message.save()
            chatroom.group_messages.add(sender_message)

            if participant != sender:
                receiver_message = Message(
                    user = participant,
                    sender = sender,
                    recipient = participant,
                    body = body,
                    is_read = False,
                    )
                receiver_message.save()
                chatroom.group_messages.add(receiver_message)

class SingleChat(models.Model):
    chat_messages = models.ManyToManyField(Message,related_name='chat_messages')
    participants = models.ManyToManyField(User,related_name='people')

    @classmethod
    def send_message(cls, single_chat, sender, recipient, body):
        messages = []
        sender_message = Message(
            user=sender,
            sender=sender,
            recipient=recipient,
            body=body,
            is_read=False,
        )
        sender_message.save()
        messages.append(sender_message)
        single_chat.chat_messages.add(sender_message)

        recipient_message = Message(
            user=recipient,
            sender=sender,
            recipient=recipient,
            body=body,
            is_read=True,
        )
        recipient_message.save()
        messages.append(recipient_message)
        single_chat.chat_messages.add(recipient_message)
        return messages

    # @property










