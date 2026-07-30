import requests
from django.conf import settings


class PawaPayService:

    def __init__(self):

        self.base_url = settings.PAWAPAY_BASE_URL

        self.headers = {
            "Authorization": (
                f"Bearer {settings.PAWAPAY_API_TOKEN}"
            ),
            "Content-Type": "application/json",
        }

    def create_deposit( self, deposit_id, amount, phone_number, provider, client_reference ):

        '''
            Fonction qui permet d'initier un paiement pawapay 
            et retourne laa reponse de la requete de paiement
        '''

        url = (
            f"{self.base_url}/v2/deposits"
        )


        payload = {
            "depositId": str(deposit_id),

            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "phoneNumber": phone_number,
                    "provider": provider,
                }
            },

            "amount": str(amount),

            "currency": settings.PAWAPAY_CURRENCY,

            "clientReferenceId": client_reference,
        }


        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            timeout=30
        )


        response.raise_for_status()

        return response.json()