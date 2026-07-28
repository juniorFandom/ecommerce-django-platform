from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .service.redis_token_service import RedisTokenBlacklistService
import logging

logger = logging.getLogger(__name__)

class AccessTokenBlacklistMiddleware:
    """
    Middleware qui vérifie à chaque requête si l'Access Token est blacklisté
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist_service = RedisTokenBlacklistService()
    
    def __call__(self, request):
        # Vérifier si la requête a un token dans l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
            
            try:
                # Vérifier si le token est blacklisté
                if self.blacklist_service.is_token_blacklisted(access_token):
                    logger.warning("Tentative d'utilisation d'un token blacklisté")
                    return JsonResponse(
                        {
                            'detail': 'Token révoqué. Veuillez vous reconnecter.',
                            'code': 'token_blacklisted'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Optionnel : Vérifier que le token est valide
                # (ne pas le faire ici pour éviter de décoder 2 fois)
                
            except Exception as e:
                logger.error(f"Erreur lors de la vérification du token: {e}")
                # On laisse passer et on laisse Django gérer l'erreur
        
        return self.get_response(request)