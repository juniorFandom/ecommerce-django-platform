from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)


class UserStatusMixin:

    def check_user_active(self, user):

        if not user.is_active:
            raise AuthenticationFailed(
                "Votre compte est désactivé."
            )


class CustomTokenObtainPairSerializer(
    UserStatusMixin,
    TokenObtainPairSerializer
):

    def validate(self, attrs):

        data = super().validate(attrs)

        self.check_user_active(self.user)

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        }

        return data


class CustomTokenRefreshSerializer(
    UserStatusMixin,
    TokenRefreshSerializer
):

    def validate(self, attrs):


        refresh = self.token_class(
            attrs['refresh']
        )

        user_id = refresh.get('user_id')

        from users.models import User

        try:
            user = User.objects.get(
                id=user_id
            )
        except User.DoesNotExist:
            raise AuthenticationFailed(
                "Utilisateur introuvable."
            )

        data = super().validate(attrs)
        self.check_user_active(user)

        return data

