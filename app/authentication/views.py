from .serializers import (
    CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
)
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .service.redis_token_service import RedisTokenBlacklistService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView  
import logging

logger = logging.getLogger(__name__)

class CustomTokenBlacklistView(TokenBlacklistView):
    """
    Vue de déconnexion personnalisée :
    - Blacklist du Refresh Token (SimpleJWT)
    - Blacklist de l'Access Token (Redis)
    - Suppression des cookies (si présents)
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        print("dans la methode de logout token ")
        user = request.user
        logger.info(f"Déconnexion demandée pour: {user.username}")
        
        # Appeler la vue parente
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # 1. Blacklister l'Access Token dans Redis
            access_token = request.auth
            if access_token:
                redis_service = RedisTokenBlacklistService()
                redis_service.blacklist_token(str(access_token))
                response.data['access_token_blacklisted'] = True
                logger.info(f"Access token blacklisté pour {user.username}")
            
            # 2. Supprimer les cookies (s'ils existent)
            # Note : delete_cookie() ne fait rien si le cookie n'existe pas
            cookies_to_delete = ['access_token', 'refresh_token', 'sessionid']
            for cookie_name in cookies_to_delete:
                if cookie_name in request.COOKIES:
                    response.delete_cookie(cookie_name)
                    logger.info(f"Cookie {cookie_name} supprimé pour {user.username}")
            
            response.data['detail'] = 'Déconnexion réussie'
            response.data['cookies_deleted'] = [
                c for c in cookies_to_delete if c in request.COOKIES
            ]
        
        return response

class CustomTokenObtainPairView( TokenObtainPairView):
    '''
     vue de login avec un serializer personnaliser qui renvoie l'access_token
     et le refresh_token ainsi que les details sur l'utilisateur (username, email, role, slug)
    '''
    serializer_class = CustomTokenObtainPairSerializer
    
    

class CustomRefreshView(TokenRefreshView):
    '''
        vue pour le refresh_token qui retourne une nouvelle paire de token
    '''
    serializer_class = CustomTokenRefreshSerializer


# Créer une vue protégée pour les tests
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Protected content'})
    
    def post(self, request):
        return Response({'message': 'Protected content'})