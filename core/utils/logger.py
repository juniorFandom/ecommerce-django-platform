import logging
import json
from datetime import datetime
from django.conf import settings

class BusinessLogger:
    """
    Logger spécialisé pour les logs métier
    """
    
    def __init__(self, module_name):
        self.logger = logging.getLogger(f'apps.{module_name}')
    
    def log_action(self, action: str, user_id: int, details: dict):
        """Log une action métier"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user_id': user_id,
            'details': details,
            'environment': settings.ENVIRONMENT
        }
        self.logger.info(f"[BUSINESS] {json.dumps(log_data)}")
    
    def log_error(self, action: str, user_id: int, error: str, context: dict = None):
        """Log une erreur métier"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user_id': user_id,
            'error': error,
            'context': context or {}
        }
        self.logger.error(f"[BUSINESS_ERROR] {json.dumps(log_data)}")

# Instances pré-configurées
auth_business_logger = BusinessLogger('authentication')
order_business_logger = BusinessLogger('commande')
payment_business_logger = BusinessLogger('paiement')
inventory_business_logger = BusinessLogger('inventory')
