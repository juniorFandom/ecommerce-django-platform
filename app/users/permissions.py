from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool( request.user.is_authenticated and request.user.role=='ADMIN')

class IsGestionnaire(BasePermission):

    def has_permission(self, request, view):
        return bool( request.user.is_authenticated and request.user.role=='GESTIONNAIRE')

class IsClient(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated, request.user.role=='CLIENT')
      
