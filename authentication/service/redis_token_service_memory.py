import logging
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)


class MemoryTokenBlacklistService:
    """
    Version purement memoire (sans Redis, sans cache Django)
    Parfait pour le developpement et les tests
    """
    
    _blacklist = {}
    
    def __init__(self):
        self.key_prefix = 'blacklist:access_token:'
        logger.warning("[WARNING] Utilisation du stockage memoire pur")
    
    def _clean_expired(self):
        """Nettoie les tokens expires"""
        now = datetime.now().timestamp()
        expired_keys = []
        
        for key, data in self._blacklist.items():
            if data.get('expires_at', 0) <= now:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._blacklist[key]
    
    def blacklist_token(self, access_token: str) -> bool:
        try:
            token_obj = AccessToken(access_token)
            exp_timestamp = token_obj.payload.get('exp')
            
            now = datetime.now().timestamp()
            ttl_remaining = int(exp_timestamp - now)
            
            if ttl_remaining <= 0:
                return False
            
            key = f"{self.key_prefix}{access_token}"
            self._blacklist[key] = {
                'value': 'blacklisted',
                'expires_at': exp_timestamp
            }
            
            self._clean_expired()
            return True
            
        except Exception as e:
            logger.error(f"Erreur: {e}")
            return False
    
    def is_token_blacklisted(self, access_token: str) -> bool:
        self._clean_expired()
        key = f"{self.key_prefix}{access_token}"
        return key in self._blacklist
    
    def remove_blacklisted_token(self, access_token: str) -> bool:
        key = f"{self.key_prefix}{access_token}"
        if key in self._blacklist:
            del self._blacklist[key]
            return True
        return False
    
    def get_stats(self) -> dict:
        self._clean_expired()
        return {
            'total_blacklisted': len(self._blacklist),
            'keys': list(self._blacklist.keys()),
            'status': 'memory_only'
        }