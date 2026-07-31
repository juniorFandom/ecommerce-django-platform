from rest_framework import serializers
from .models import Facture
from commande.models import Commande
from commande.serializer import CommandeSerializer



class FactureSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Facture
        fields = ['commande','montant']


    def create(self, validated_data):
        commande_id = validated_data['commande'].id
        montant = validated_data['montant']

        commande = Commande.objects.get(id=commande_id)
        if commande.montant != montant:
            raise serializers.ValidationError(
                "le montant de la commande ne correspond pas"
            )

        facture = Facture.objects.create(**validated_data)

        return facture



class FactureDetailSerializer(serializers.ModelSerializer):
    commande = CommandeSerializer(read_only=True)
    class Meta:
        model = Facture
        fields = '__all__'