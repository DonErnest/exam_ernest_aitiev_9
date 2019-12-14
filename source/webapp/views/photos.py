from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Photo


class IndexView(ListView):
    template_name = 'index.html'
    model = Photo
    ordering = ['-created_at']


class PhotoDetailedView(DetailView):
    model = Photo
    template_name = 'photo/photo_detailed.html'


class PhotoCreateView(CreateView):
    model = Photo
    template_name = 'photo/photo_create.html'


    def get_success_url(self):
        return reverse('webapp:photo_detailed', kwargs = {'pk': self.object.pk})


class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ['photo', 'description']
    template_name = 'photo/photo_update.html'

    def get_success_url(self):
        return reverse('webapp:photo_detailed', kwargs={'pk': self.object.pk})

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'

    def get_success_url(self):
        return reverse('webapp:main_page')

