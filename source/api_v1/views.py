import django_filters
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

from api_v1.permissions import CommentAuthorOrReadOnly, LikeAuthenticatedAddOnly
from api_v1.serializers import UserSerializer, CommentSerializer, LikeSerializer
from webapp.models import Comment, Photo, Like


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentAuthorOrReadOnly | DjangoModelPermissions]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # filterset_fields = ['photo']

    def create(self, request, *args, **kwargs):
        pk = request.data.get('photo')
        photo = Photo.objects.get(pk=pk)
        if self.queryset.filter(photo=photo):
            return Response({'error': 'you cannot like the same photo twice' }, status=400)
        photo.likes += 1
        photo.save()
        return super(LikeViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        photo = Photo.objects.get(pk=instance.photo.pk)
        photo.likes -= 1
        photo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer  = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'response': 'Регистрация прошла успешно!',
                             'first_name': user.first_name,
                             'last_name': user.last_name})
        else:
            return Response({serializer.errors})



class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok', 'message':'Вы вышли'})