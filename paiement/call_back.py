from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Paiement


@api_view(["POST"])
def pawapay_callback(request):

    data = request.data

    print("Callback PawaPay reçu :")
    print(data)


    deposit_id = data.get(
        "depositId"
    )

    paiement_status = data.get(
        "status"
    )


    try:

        paiement = Paiement.objects.get(
            pawapay_id=deposit_id
        )

    except Paiement.DoesNotExist:

        return Response(
            {
                "error": "Paiement introuvable"
            },
            status=status.HTTP_404_NOT_FOUND
        )


    if paiement_status == "COMPLETED":

        paiement.statut = "SUCCESS"

        paiement.save(
            update_fields=[
                "statut"
            ]
        )


        commande = paiement.commande

        commande.statut = "PAYEE"

        commande.save(
            update_fields=[
                "statut"
            ]
        )


    elif paiement_status == "FAILED":

        paiement.statut = "FAILED"

        paiement.save(
            update_fields=[
                "statut"
            ]
        )

    elif paiement.montant != data["amount"]:

        return Response(
            {
                "error":"Montant invalide"
            },
            status=400
        )

    return Response(
        {
            "message": "Callback reçu"
        },
        status=status.HTTP_200_OK
    )