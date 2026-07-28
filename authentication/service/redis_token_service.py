import logging
from datetime import datetime
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken

# Configurer le logging pour éviter les erreurs d'encodage
logger = logging.getLogger(__name__)

# Forcer l'encodage UTF-8 pour les logs sur Windows
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class RedisTokenBlacklistService:
    """
    Service pour gerer la blacklist des access tokens via Redis
    Utilise le systeme de cache Django (django-redis)
    """
    
    def __init__(self):
        self.key_prefix = 'blacklist:access_token:'
        
        # Verifier si on utilise un cache memoire
        self._is_memory_cache = self._check_if_memory_cache()
        
        if self._is_memory_cache:
            logger.warning("[WARNING] Utilisation du cache memoire (pas de Redis). Les tokens seront perdus au redemarrage.")
        else:
            logger.info("[OK] Cache Redis detecte et fonctionnel.")
    
    def _check_if_memory_cache(self) -> bool:
        """Verifie si le cache est un cache memoire (LocMemCache)"""
        try:
            from django.core.cache import caches
            backend = caches['default'].__class__.__name__
            return 'LocMemCache' in backend or 'DummyCache' in backend
        except Exception:
            return True
    
    def blacklist_token(self, access_token: str) -> bool:
        """
        Ajoute un access token à la blacklist Redis avec son TTL restant
        """
        try:
            token_obj = AccessToken(access_token)
            exp_timestamp = token_obj.payload.get('exp')
            
            now = datetime.now().timestamp()
            ttl_remaining = int(exp_timestamp - now)
            
            if ttl_remaining <= 0:
                logger.info("Token deja expire, pas besoin de blacklist")
                return False
            
            key = f"{self.key_prefix}{access_token}"
            cache.set(key, 'blacklisted', timeout=ttl_remaining)
            
            logger.info(f"[OK] Token blackliste pour {ttl_remaining} secondes")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du blacklist du token: {e}")
            return False
    
    def is_token_blacklisted(self, access_token: str) -> bool:
        """
        Verifie si un access token est dans la blacklist Redis
        """
        key = f"{self.key_prefix}{access_token}"
        is_blacklisted = cache.get(key) is not None
        
        if is_blacklisted:
            logger.debug("[LOCK] Token blackliste detecte")
        
        return is_blacklisted
    
    def remove_blacklisted_token(self, access_token: str) -> bool:
        """
        Supprime un token de la blacklist (utile pour les tests)
        """
        key = f"{self.key_prefix}{access_token}"
        try:
            cache.delete(key)
            logger.info(f"[OK] Token supprime de la blacklist: {access_token[:20]}...")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression: {e}")
            return False
    
    def get_ttl(self, access_token: str) -> int:
        """
        Recupere le TTL restant d'un token blackliste
        Retourne:
        - > 0 : TTL restant en secondes
        - -1 : La clé existe mais n'a pas de TTL
        - -2 : La clé n'existe pas
        """
        key = f"{self.key_prefix}{access_token}"
        
        try:
            from django_redis import get_redis_connection
            redis_client = get_redis_connection("default")
            ttl = redis_client.ttl(key)
            return ttl
        except Exception as e:
            logger.error(f"Erreur lors de la recuperation du TTL: {e}")
            return -2
    
    def get_all_blacklisted(self) -> list:
        """
        Recupere tous les tokens blacklistes (utile pour le debug)
        """
        try:
            if self._is_memory_cache:
                logger.warning("[WARNING] Listing des tokens non disponible avec le cache memoire")
                return []
            
            from django_redis import get_redis_connection
            redis_client = get_redis_connection("default")
            
            pattern = f"{self.key_prefix}*"
            keys = redis_client.keys(pattern)
            
            return [key.replace(self.key_prefix, '') for key in keys]
        except Exception as e:
            logger.error(f"Erreur lors de la recuperation des tokens: {e}")
            return []
    
    def get_stats(self) -> dict:
        """
        Recupere des statistiques sur la blacklist
        """
        try:
            if self._is_memory_cache:
                return {
                    'status': 'memory_cache',
                    'message': 'Utilisation du cache memoire (pas de Redis)',
                    'total_blacklisted': 'inconnu',
                    'warning': 'Les tokens sont perdus au redemarrage'
                }
            
            from django_redis import get_redis_connection
            redis_client = get_redis_connection("default")
            
            pattern = f"{self.key_prefix}*"
            keys = redis_client.keys(pattern)
            
            return {
                'status': 'redis',
                'total_blacklisted': len(keys),
                'keys': keys,
            }
        except Exception as e:
            logger.error(f"Erreur lors de la recuperation des stats: {e}")
            return {'error': str(e)}