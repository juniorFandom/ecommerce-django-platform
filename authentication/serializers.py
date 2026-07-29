from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)
from users.models import User


class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    def validate(self, attrs):

        data = super().validate(attrs)
        print("dans le serializer d'obtention de la paire de token ")
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'slug': self.user.slug
        }

        return data


class CustomTokenRefreshSerializer(
    TokenRefreshSerializer
):

    def validate(self, attrs):

        print("dans le serializer de refresh du token ")


        refresh = self.token_class(
            attrs['refresh']
        )

        user_id = refresh.get('user_id')

        try:
            user = User.objects.get(
                id=user_id
            )
        except User.DoesNotExist:
            raise AuthenticationFailed(
                "Utilisateur introuvable."
            )
        if not user.check_user_active:
            raise AuthenticationFailed(
                "Votre compte est désactivé."
            )
        data = super().validate(attrs)

        return data

