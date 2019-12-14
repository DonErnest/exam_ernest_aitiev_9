from rest_framework import permissions


class CommentAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if 'pk' in view.kwargs and view.kwargs['pk']:
            obj = view.get_object()
            if request.method in permissions.SAFE_METHODS:
                return True
            return bool(obj.author.pk == request.user.pk)
        else:
            if request.method not in permissions.SAFE_METHODS:
                return request.user.is_authenticated
            return True


class LikeAuthenticatedAddOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return True
