from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import UserSerializer, UserDetailSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import User 

class UserGenericAPIView(GenericAPIView):
    serializer_class =  UserSerializer
    lookup_field = 'slug'
    query = User.objects.all()

class UserCreateAPIView(UserGenericAPIView, CreateModelMixin):
    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserListAPIView(UserGenericAPIView, ListModelMixin):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserUpdateAPIView(UserGenericAPIView, UpdateModelMixin):
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **Kwargs):
        return self.update(request, *args, **kwargs)

class UserDestroyAPIView(UserGenericAPIView, DestroyModelMixin):

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserRetreiveAPIView(UserGenericAPIView, RetrieveModelMixin):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserAllDetailAPIView(UserGenericAPIView, RetrieveModelMixin):
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args , **kwargs)