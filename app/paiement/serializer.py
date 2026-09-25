from rest_framework import serializers

from .models import Paiement
from .service.service import PawaPayService


class PaiementSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = Paiement

        fields = [
            # "id",
            "commande",
            "reference",
            # "montant",
            "moyen",
            # "statut",
            # "created_at",
            "phone",
        ]

        # read_only_fields = [
        #     "id",
        #     "reference",
        #     "montant",
        #     "statut",
        #     "created_at",
        # ]


    def validate_commande(self, commande):

        if commande.montant <= 0:
            raise serializers.ValidationError(
                "Le montant de la commande doit être supérieur à zéro."
            )

        if hasattr(commande, "paiement"):
            raise serializers.ValidationError(
                "Cette commande possède déjà un paiement."
            )

        return commande


    def validate_phone(self, phone):
        if phone is None:
            phone = self.context.get("request").user.phone

        if phone and not str(phone).isdigit():
            raise serializers.ValidationError({
                "phone": "Le numéro de téléphone doit être un entier positif."
            })

        if phone[0] != '6':
            raise serializers.ValidationError({
                "phone": "Le numéro de téléphone doit commencer par '6'."
            })

        return phone


    def create(self, validated_data):

        commande = validated_data.pop(
            "commande"
        )

        phone = validated_data.pop(
            "phone"
        )

        paiement = Paiement.objects.create(

            commande=commande,

            montant=commande.montant,

            moyen="PAWAPAY",

            statut="PENDING",

        )


        pawapay = PawaPayService()


        try:

            response = pawapay.create_deposit(

                deposit_id=paiement.reference,

                amount=paiement.montant,

                phone=phone,

            )


        except Exception as e:

            paiement.statut = "FAILED"

            paiement.save(
                update_fields=["statut"]
            )

            raise serializers.ValidationError({

                "paiement":
                    f"Impossible d'initier le paiement : {str(e)}"

            })


        status = response.get(
            "status"
        )


        if status in [
            "ACCEPTED",
            "ACCEPT",
        ]:

            paiement.pawapay_id = response.get(
                "depositId",
                paiement.reference
            )

            paiement.statut = "PENDING"

            paiement.save(

                update_fields=[
                    "pawapay_id",
                    "statut",
                ]

            )


        elif status in [
            "FAILED",
            "REJECTED",
        ]:

            paiement.statut = "FAILED"

            paiement.save(
                update_fields=["statut"]
            )


        return paiement
            
        
        
