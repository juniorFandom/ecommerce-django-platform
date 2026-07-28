from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from authentication.middleware import AccessTokenBlacklistMiddleware
from authentication.service.redis_token_service import RedisTokenBlacklistService


User = get_user_model()



class AccessTokenBlacklistMiddlewareTest(TestCase):
    """Tests du middleware de blacklist"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AccessTokenBlacklistMiddleware(lambda req: JsonResponse({'ok': True}))
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.service = RedisTokenBlacklistService()
    
    def test_valid_token_passes(self):
        """Test qu'un token valide passe le middleware"""
        access_token = str(AccessToken.for_user(self.user))
        
        request = self.factory.get('/api/test/')
        request.headers = {'Authorization': f'Bearer {access_token}'}
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 200)
    
    def test_blacklisted_token_blocked(self):
        """Test qu'un token blacklisté est bloqué"""
        access_token = str(AccessToken.for_user(self.user))
        
        self.service.blacklist_token(access_token)
        
        request = self.factory.get('/api/test/')
        request.headers = {'Authorization': f'Bearer {access_token}'}
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 401)
    
    def test_no_token_passes(self):
        """Test qu'une requête sans token passe le middleware"""
        request = self.factory.get('/api/test/')
        request.headers = {}
        
        response = self.middleware(request)
        
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_token_handled(self):
        """Test qu'un token invalide est géré"""
        request = self.factory.get('/api/test/')
        request.headers = {'Authorization': 'Bearer invalid.token.here'}
        
        response = self.middleware(request)
        
        # Le middleware devrait laisser passer et laisser Django gérer
        self.assertEqual(response.status_code, 200)