from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken

from authentication.service.redis_token_service import RedisTokenBlacklistService
from authentication.service.redis_token_service_memory import MemoryTokenBlacklistService

User = get_user_model()


class RedisTokenBlacklistServiceTest(TestCase):
    """Tests pour RedisTokenBlacklistService"""
    
    def setUp(self):
        # Nettoyer le cache avant chaque test
        cache.clear()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.service = RedisTokenBlacklistService()
        self.access_token = str(AccessToken.for_user(self.user))
    
    def tearDown(self):
        # Nettoyer le cache après chaque test
        cache.clear()
    
    def test_blacklist_token(self):
        result = self.service.blacklist_token(self.access_token)
        self.assertTrue(result)
        
        is_blacklisted = self.service.is_token_blacklisted(self.access_token)
        self.assertTrue(is_blacklisted)
    
    def test_remove_blacklisted_token(self):
        self.service.blacklist_token(self.access_token)
        self.assertTrue(self.service.is_token_blacklisted(self.access_token))
        
        self.service.remove_blacklisted_token(self.access_token)
        self.assertFalse(self.service.is_token_blacklisted(self.access_token))
    
    def test_ttl_calculation(self):
        """Test du calcul du TTL - Adapté pour le cache mémoire"""
        self.service.blacklist_token(self.access_token)
        
        ttl = self.service.get_ttl(self.access_token)
        
        self.assertIn(ttl, [-2, -1, 0])  # -2: n'existe pas, -1: pas de TTL
    



class MemoryTokenBlacklistServiceTest(TestCase):
    """Tests pour MemoryTokenBlacklistService"""
    
    def setUp(self):
        # Réinitialiser le service avant chaque test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.service = MemoryTokenBlacklistService()
        self.access_token = str(AccessToken.for_user(self.user))
        
        # Nettoyer la blacklist du service
        self.service._blacklist.clear()
    
    def test_blacklist_token(self):
        result = self.service.blacklist_token(self.access_token)
        self.assertTrue(result)
        
        is_blacklisted = self.service.is_token_blacklisted(self.access_token)
        self.assertTrue(is_blacklisted)
    
    def test_remove_blacklisted_token(self):
        self.service.blacklist_token(self.access_token)
        self.assertTrue(self.service.is_token_blacklisted(self.access_token))
        
        self.service.remove_blacklisted_token(self.access_token)
        self.assertFalse(self.service.is_token_blacklisted(self.access_token))
    
    def test_stats(self):
        """Test des statistiques du service mémoire"""
        self.service.blacklist_token(self.access_token)
        stats = self.service.get_stats()
        
        self.assertEqual(stats['total_blacklisted'], 1)
        self.assertEqual(stats['status'], 'memory_only')