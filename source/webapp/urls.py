from django.urls import path

from webapp.views import IndexView, PhotoDetailedView, PhotoCreateView, PhotoUpdateView, login_view, LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('photos/<int:pk>/', PhotoDetailedView.as_view(), name='photo_detailed'),
    path('photos/<int:pk>/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/add/', PhotoCreateView.as_view(), name='photo_add'),

    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

app_name='webapp'