from rest_framework import serializers
from .service.service import PawaPayService
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):

    class Meta:

        model = Paiement

        fields = [
            "id",
            "commande",
            "reference",
            "montant",
            "moyen",
            "statut",
            "created_at"
        ]

        read_only_fields = [
            'id'
            "reference",
            "montant",
            "statut",
            "created_at"
        ]

    def create(self, validated_data):
        commande = validated_data.pop('commande')
        response = PawaPayService().create_deposit( **validated_data )
        
