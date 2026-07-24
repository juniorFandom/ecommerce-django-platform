from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import UserSerializer, UserDetailSerializer, ChangePasswordSerializer
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import User 
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdmin, IsGestionnaire, IsClient
from drf_spectacular.utils import extend_schema


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


class UserDeactivateAPIView(UserGenericAPIView):

    def post(self, request, slug):

        user = self.get_object()

        user.is_active = False
        user.save(update_fields=['is_active'])

        return Response(
            {
                'message': 'Utilisateur désactivé avec succès.'
            },
            status=status.HTTP_200_OK
        )


class UserActivateAPIView(UserGenericAPIView):

    def post(self, request, slug):

        user = self.get_object()

        user.is_active = True
        user.save(update_fields=['is_active'])

        return Response(
            {
                'message': 'Utilisateur activé avec succès.'
            },
            status=status.HTTP_200_OK
        )



class UserChangePasswordAPIView(APIView):

    # permission_classes = [
    #     IsAuthenticated
    # ]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    )
    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                'message':
                'Mot de passe modifié avec succès.'
            },
            status=status.HTTP_200_OK
        )