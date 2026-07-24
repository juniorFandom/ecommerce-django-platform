from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .serializers import (
    CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
)


class CustomTokenObtainPairView( TokenObtainPairView):
 
    serializer_class = (
        CustomTokenObtainPairSerializer
    )

class CustomRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenBlacklistView(TokenBlacklistView):
    pass

