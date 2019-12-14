from django.urls import path

from webapp.views import IndexView, PhotoDetailedView, PhotoCreateView, PhotoUpdateView, UserLoginView, UserLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('photos/<int:pk>/', PhotoDetailedView.as_view(), name='photo_detailed'),
    path('photos/<int:pk>/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/add/', PhotoCreateView.as_view(), name='photo_add'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout')
]

app_name='webapp'