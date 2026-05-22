from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from chat.forms import MessageForm, ChatForm
from chat.models import Message, ChatRoom, SingleChat
from django.contrib.auth.models import User
from person.models import *
from user.models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from notifications.signals import notify
from notifications.models import Notification



# Create your views here.
@login_required
def inbox(request, reciver ):
    user = request.user
    profile = Profile.objects.filter(user=request.user).values('bio', 'profile_picture').first()
    inbox_to = User.objects.get(username=reciver)
    rec_profile = Profile.objects.filter(user=inbox_to).values('bio', 'profile_picture').first()
    recipient = User.objects.get(username=reciver)

    single_chat = SingleChat.objects.filter(participants=user).filter(participants=recipient).first()
    # added
    if single_chat is None:
        single_chat = SingleChat.objects.create()
        single_chat.participants.add(user, recipient)
        single_chat = SingleChat.objects.filter(participants=request.user).filter(participants=recipient).first()

    # if request.method == "POST":
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         body = form.cleaned_data['body']
    #         try:
    #             messages = SingleChat.send_message(single_chat,user,recipient ,body)
    #             for message in messages:
    #                 single_chat.chat_messages.add(message)
    #
    #         except User.DoesNotExist:
    #             print("User does not exist")
    # added

    messages= single_chat.chat_messages.filter(user=user).order_by('date')
    reciver_messages = single_chat.chat_messages.exclude(user=user).order_by('date')

    for message in reciver_messages:
        message.is_read = True
        message.save()

    context = {
        'user': user,
        'recipient': inbox_to,
        'profile': profile,
        'recipient_profile': rec_profile,
        'all_messages': messages,
        'single_chat': single_chat,
        'inbox-to' :inbox_to,
        'reciver': reciver,
        'reciver_messages': reciver_messages,

    }

    # if single_chat:
    #     messages_to = single_chat.chat_messages.filter(user=user, recipient=inbox_to, sender=user).order_by('-date')
    #     messages_from = single_chat.chat_messages.filter(user=inbox_to, sender=inbox_to, recipient=user).order_by('-date')
    #     messages_all = single_chat.chat_messages.filter(Q(user=user) | Q(user=inbox_to)).order_by('date')
    #     context = {
    #         'user': user,
    #         'recipient': inbox_to,
    #         'profile': profile,
    #         'recipient_profile': rec_profile,
    #         'messages_to': messages_to,
    #         'messages_from': messages_from,
    #         'messages_all': messages_all,
    #     }
    # else:
    #     context = {
    #         'user': user,
    #         'recipient': inbox_to,
    #         'profile': profile,
    #         'recipient_profile': rec_profile,
    #     }

    return render(request, 'inbox.html',context)
@login_required
def inboxlist(request):
    user = request.user
    profile = Profile.objects.filter(user=user).values('bio', 'profile_picture').first()
    chatrooms = ChatRoom.objects.filter(participants=user)
    messages = Message.objects.filter(
        Q(user=user, sender=user) | Q(user=user, recipient=user)
    )

    u_users = set()
    for message in messages:
        if message.sender != user:
            u_users.add(message.sender)
        if message.recipient != user:
            u_users.add(message.recipient)
    for u in user.profile.followers.all():
        u_users.add(u)
    u_users= set(u_users)

    unread=[]
    for u in u_users:
        chat= SingleChat.objects.filter(participants=u).filter(participants=user).first()
        unread.append({
           'unread' :chat.chat_messages.filter(is_read=False,user=u, recipient=request.user,sender=u).count(),
            'user':u


        })
        #
        # message_unread =[]
        # for user, count in u_users,unread:
        #     message_unread.append({'user':user,'count': count } )


    context = {
               'user':user,
               'profile':profile,
               'prev_messes':u_users,
                'chatrooms':chatrooms,
                'message_unread': unread
               }
    return render(request, 'inboxlist.html', context)

class CreateGroup(LoginRequiredMixin, CreateView):
    model=ChatRoom
    form_class = ChatForm
    template_name = 'creategroup.html'
    success_url = reverse_lazy('chat:inboxlist')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context= super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
@login_required
def chatroom_messages(request, pk):
    user = request.user
    chatroom = ChatRoom.objects.get(id=pk)
    profile = Profile.objects.filter(user=request.user).values('bio', 'profile_picture').first()
    user_messages = Message.objects.filter(Q(user=user, sender=user) | Q(user=user, recipient=user))

    if user in chatroom.participants.all():
        messages_from_user = chatroom.group_messages.filter(sender=user, user=user,recipient=user)
        messages_to_user = chatroom.group_messages.filter(recipient=user, user=user)
        all_messages = chatroom.group_messages.filter( user=user).order_by('date')
    else:
        all_messages=[]
        messages_from_user = []
        messages_to_user = []

    # if request.method == "POST":
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         body = form.cleaned_data['body']
    #         try:
    #             participants = chatroom.participants.all()
    #             ChatRoom.send_message(chatroom,user, participants, body)
    #         except User.DoesNotExist:
    #             print("User does not exist")



    context = {'chatroom':chatroom,
               'user':user,
               'profile':profile,
               'all_messages':all_messages,
               'messages_from_user':messages_from_user,
               'messages_to_user':messages_to_user,
               'group_chat': chatroom,
               }
    return render(request, 'chatroom.html', context)

class EditChatRoom(LoginRequiredMixin, UpdateView):
    model = ChatRoom
    form_class = ChatForm
    template_name = 'editchatroom.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['chatroom']=ChatRoom.objects.get(pk=self.kwargs['pk'])
        return context
    def get_success_url(self):
        return reverse_lazy('chat:inboxlist')

class DeleteChatroom(LoginRequiredMixin, DeleteView):
    model = ChatRoom
    template_name = 'deletechatroom.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    def get_context_data(self, **kwargs):
        context= super().get_context_data()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['chatroom']=ChatRoom.objects.get(id=self.kwargs['pk'])
        return context
    #
    def get_success_url(self):
        return reverse_lazy('chat:inboxlist',
                            kwargs={'pk': self.object.created_by.username,
                                    'action_type': ' '})

    #
    #

#notifications views


@login_required
def notifications_view(request):
    profile= Profile.objects.filter(user=request.user).values('bio', 'profile_picture').first()
    notifications = Notification.objects.filter(recipient=request.user).unread()
    context = {'notifications':notifications,'profile':profile}
    return render(request, 'notifications.html', context)

@login_required
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    print(f"Marking notification {notification_id} as read")
    notification.mark_as_read()
    return JsonResponse({'status': 'success'})

