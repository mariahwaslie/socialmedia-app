from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from notifications.signals import notify
from chat.models import ChatRoom
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from notifications.models import Notification
from person.models import Post

@login_required
def create_group_request(request):
    if request.method == 'POST':
        form = GroupCreationRequestForm(request.POST)
        if form.is_valid():
            group_request = form.save(commit=False)
            group_request.user = request.user
            group_request.save()
            messages.success(request, 'Your request to create a group has been submitted.')
            return redirect('person:following')  # Redirect to a list of groups or a success page
    else:
        form = GroupCreationRequestForm()

    return render(request, 'create_group_request.html', {'form': form})


@login_required
def create_church_request(request):
    if request.method == 'POST':
        form = ChurchCreationRequestForm(request.POST)
        if form.is_valid():
            group_request = form.save(commit=False)
            group_request.user = request.user
            group_request.save()
            messages.success(request, 'Your request to create a Church  has been submitted.')
            return redirect('person:following')  # Redirect to a list of groups or a success page
    else:
        form = ChurchCreationRequestForm()

    return render(request, 'church_request.html', {'form': form})

@staff_member_required
def review_group_requests(request):
    pending_requests = GroupCreationRequest.objects.filter(reviewed=False)
    pending_church_request =ChurchCreationRequest.objects.filter(reviewed=False)
    context = {
        'pending_requests': pending_requests,
        'pending_church_request': pending_church_request,
    }
    return render(request, 'review_group_requests.html', context)

@staff_member_required
def approve_group_request(request, request_id):
    group_request = get_object_or_404(GroupCreationRequest, id=request_id)
    if request.method == 'POST':
        form= ApproveGroupCreation(request.POST)
        if form.is_valid():
        # Create the actual group
            group = Group.objects.create(
                name=group_request.group_name,
                description=group_request.description,
                privacy=group_request.privacy
            )
            group.members.add(group_request.user)  # Add the requester as a member
            member=GroupMembership.objects.get(group=group, user=request.user)
            member.role='admin'
            member.save()
            group_request.reviewed = True
            group_request.approved = True
            group_request.save()
            notify.send(
                request.user,
                recipient=group_request.user,
                verb='Group Approved',
                description=f'Your Group {group.name}  has been approved',
            )
            groupchat = ChatRoom.objects.create(
                name=group.name,
                created_by=group_request.user,
                description=group_request.description,
                group=group

            )

            groupchat.participants.add(group_request.user)
            groupchat.save()

            return redirect('faith:review_group_requests')
    else:
        form = ApproveGroupCreation()
    context={
        'form': form,
        'group_request': group_request
    }

    return render(request,
                  'approve.html', context)

@staff_member_required
def deny_group_request(request, request_id):
    group_request = get_object_or_404(GroupCreationRequest, id=request_id)
    if request.method == 'POST':
        group_request.reviewed = True
        group_request.approved = False
        group_request.save()
        messages.info(request, f"The request for group '{group_request.group_name}' has been denied.")
        return redirect('faith:review_group_requests')

    return render(request, 'deny.html', {'group_request': group_request})

def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    admins = GroupMembership.objects.filter(role='admin', user=request.user)
    requests_to_join = GroupRequest.objects.filter(group=group, reviewed=False)
    posts = BlogPost.objects.filter(group=group)
    group_chat = ChatRoom.objects.get(group=group)
    events= Event.objects.filter(group=group).all()
    prayers = Post.objects.filter(group=group)
    images =Image.objects.filter(group=group)
    videos=Video.objects.filter(group=group)

    context={
        'group': group,
        'admins': admins,
        'request_to_join': requests_to_join,
        'posts': posts,
        'group_chat': group_chat,
        'events':events,
        'prayers' : prayers,
        'videos':videos,
        'images':images
    }
    return render(request,'group_detail.html', context )

@login_required
def group_list(request):
    groups = Group.objects.all()
    context= {'groups':groups}
    return render(request, 'group_list.html', context)

@login_required
def join_group(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    join_user = User.objects.get(id=user_id)
    if GroupRequest.objects.filter(group=group, user=join_user):
        GroupRequest.objects.filter(group=group, user=join_user).update(reviewed=True)
    if not group.is_member(join_user):
        GroupMembership.objects.create(
            group=group,
            user=join_user,
            role='member'
        )
        joinchat = ChatRoom.objects.get(name=group.name)
        joinchat.participants.add(join_user)
        joinchat.save()
    else:
        messages.info(request, "You are already a member of this group.")

    return redirect('faith:group_details', group_id=group_id)

# this creates a request for the user to join the group
@login_required
def request_to_join(request, group_id ):
    group= get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        if 'request_to_join' in request.POST:
            form = GroupRequestForm(request.POST)
            if form.is_valid():
                request_to_join = form.save(commit=False)
                request_to_join.user = request.user
                request_to_join.group = group
                request_to_join.save()

                return redirect('faith:group_details', group_id=group_id)

@login_required
def deny_group_join(request, group_id ):
    group= get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        if 'request_denied' in request.POST:
            GroupRequest.objects.filter(group=group, user=request.user).update(reviewed=True)
        return redirect('group_details', group_id=group_id)

@login_required
def create_post(request, group_id =None):
    if group_id:
        group = Group.objects.get(id=group_id)
        if not group.is_member(request.user):
            messages.error(request, "You are not a member of this group.")
            return redirect('faith:group_details', group_id=group_id)

        if request.method == 'POST':
            form = GroupPostForm(request.POST, group=group)
            if form.is_valid():
                post = form.save(commit=False)
                post.created_by = request.user
                post.group = group
                post.save()
                return redirect("faith:group_details", group_id=group_id)
        else:
            form= GroupPostForm(group=group)
        return render(request, 'createblogpost.html', {'form':form, 'group':group})
@login_required
def create_prayer(request, group_id=None):
    if group_id:
        group = Group.objects.get(id=group_id)
        if not group.is_member(request.user):
            messages.error(request, "You are not a member of this group.")
            return redirect('faith:group_details', group_id=group_id)
        if request.method == 'POST':
            form = GroupPrayerForm(request.POST, group=group)
            if form.is_valid():
                prayer = form.save(commit=False)
                prayer.user = request.user
                prayer.group = group
                prayer.save()
                return redirect('faith:group_details', group_id=group_id)
        else:
            form= GroupPrayerForm(group=group)
        return render(request,'createprayer.html',{'form':form, 'group':group})

def create_video(request, group_id=None):
    if group_id:
        group = Group.objects.get(id=group_id)
        if not group.is_member(request.user):
            messages.error(request, "You are not a member of this group.")
            return redirect('faith:group_details', group_id=group_id)
        if request.method == 'POST':
            form = GroupVideoForm(request.POST,request.FILES, group=group)
            if form.is_valid():
                vid = form.save(commit=False)
                vid.user = request.user
                vid.group = group
                vid.save()
                return redirect('faith:group_details',group_id=group_id)
        else:
            form= GroupVideoForm(group=group)
        return render(request, 'createvideo.html',{'form':form, 'group':group})


def create_image(request, group_id=None):
    if group_id:
        group = Group.objects.get(id=group_id)
        if not group.is_member(request.user):
            messages.error(request, "You are not a member of this group.")
            return redirect('faith:group_details', group_id=group_id)
        if request.method == 'POST':
            form = GroupImageForm(request.POST,request.FILES, group=group)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.group = group
                image.save()
                return redirect('faith:group_details',group_id=group_id)
        else:
            form= GroupImageForm(group=group)
        return render(request, 'createimage.html',{'form':form, 'group':group})
@login_required
def create_event(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.group = group
            form.save()
            return redirect('faith:group_details', group_id=group_id)
    else:
        form = EventForm()

    return render(request, 'eventform.html', {'form': form})
@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)  # Redirect to the event detail page
    else:
        form = EventForm(instance=event)

    return render(request, 'eventform.html', {'form': form})
#
#
# #function to geocode the address
# def geocode_address(address):
#     geolocator = Nominatim(user_agent='faithgroups')
#     location = geolocator.geocode(address)
#     if location:
#         return Point(location.longituide, location.latituide)
#
#
# def create_location_from_address(request):
#     if request.method == 'POST':
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         add = request.POST.get('address')
#         address = f"{add}, {city}, {state}, {zip_code}"
#
#         # location_point = geocode_address(address)
#
#     #     if location_point:
#     #         Location.objects.create(location_field=location_point,
#     #                                 city=city, state=state, zip_code=zip_code,
#     #                                 address=add)
#     # else:
#         # Handle GET request or render form
#         pass
#
#
#
# class LocationView(ListView):
#     template_name = 'locationview.html'
#
#
#     def get(self, request, pk ):
#         location = Location.objects.get(pk=pk)
#         context= {
#             'location': location
#         }
#         return render(request, self.template_name, context)
#
#







