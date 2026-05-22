from django.shortcuts import render
from .forms import  *
from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, PlaylistItem
from django.contrib.auth.decorators import login_required
from person.models import video
from django.views.generic import CreateView, DetailView, FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'create_playlist.html'
    success_url = reverse_lazy('playlist_list')  # Redirect after successful creation

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def add_to_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    if request.method == 'POST':
        form = PlaylistItemForm(request.POST)
        if form.is_valid():
            playlist_item = form.save(commit=False)
            playlist_item.playlist = playlist
            playlist_item.save()
            return redirect('playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistItemForm()
    return render(request, 'add_to_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    playlist_items = playlist.playlist_video_items.all()
    context={'playlist': playlist,
             'playlist_items': playlist_items}
    return render(request, 'playlistdetail.html',
                  context)
