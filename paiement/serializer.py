from rest_framework import serializers
from .service import PawaPayService
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:

        model = Paiement

        fields = [
            "id",
            "commande",
            "reference",
            "montant",
            "moyen",
            "statut",
            "created_at",
            'phone'
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
        paiement= PawaPayService()
        response = paiement.create_deposit( **validated_data )

        if response['status'] == 'ACCEPT':
            
        
        
