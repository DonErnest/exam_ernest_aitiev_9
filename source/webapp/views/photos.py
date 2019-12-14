from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Photo


class IndexView(ListView):
    template_name = 'index.html'
    model = Photo
    ordering = ['-created_at']
    context_object_name = 'photos'


class PhotoDetailedView(DetailView):
    model = Photo
    template_name = 'photo/photo_detailed.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PhotoDetailedView, self).get_context_data()
    #     context['comments'] = self.object.comments.all()
    #     return context


class PhotoCreateView(CreateView):
    model = Photo
    template_name = 'photo/photo_create.html'
    fields = ['photo', 'description']

    def get_success_url(self):
        return reverse('webapp:photo_detailed', kwargs = {'pk': self.object.pk})

    def form_valid(self, form):
        self.object = Photo.objects.create(author = self.request.user, photo = form.cleaned_data['photo'],
                                           description=form.cleaned_data['description'])
        return HttpResponseRedirect(self.get_success_url())


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

