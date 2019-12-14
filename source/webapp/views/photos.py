from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('webapp:login')
        return super(PhotoCreateView, self).dispatch(request, *args, **kwargs)

class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ['photo', 'description']
    template_name = 'photo/photo_update.html'

    def get_success_url(self):
        return reverse('webapp:photo_detailed', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('webapp.change_photo') or self.object.author != request.user:
            raise PermissionDenied('403 Forbidden')
        return super(PhotoUpdateView, self).dispatch(request, *args, **kwargs)

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'

    def get_success_url(self):
        return reverse('webapp:main_page')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('webapp.delete_photo') or self.object.author != request.user:
            raise PermissionDenied('403 Forbidden')
        return super(PhotoDeleteView, self).dispatch(request, *args, **kwargs)