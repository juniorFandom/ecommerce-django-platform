from django.test import TestCase
from decimal import Decimal
from categorie.models import Category
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product
from inventory.models import Inventory
from .models import Commande, LigneCommande


User = get_user_model()


class CommandeAPITestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="junior",
            email="junior@test.com",
            password="password123"
        )

        self.client.force_authenticate(self.user)
        self.categorie = Category.objects.create(name='test')

        self.product = Product.objects.create(
            category = self.categorie,
            name="Ordinateur",
            prix=Decimal("250000")
        )

        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity=20,
            reserved_quantity=0,
            minimum_stock=5
        )

        self.create_url = reverse("commande-create")
        self.list_url = reverse("commande-list")

    def test_create_commande(self):

        payload = {
            "lignes": [
                {
                    "product": self.product.id,
                    "quantity": 2
                }
            ]
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        print("STATUS:", response.status_code)
        print("DATA:", response.data)   

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Commande.objects.count(),
            1
        )

        self.assertEqual(
            LigneCommande.objects.count(),
            1
        )

    def test_reserved_quantity_updated(self):

        payload = {
            "lignes": [
                {
                    "product": self.product.id,
                    "quantity": 3
                }
            ]
        }

        self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.inventory.refresh_from_db()

        self.assertEqual(
            self.inventory.reserved_quantity,
            3
        )

    def test_create_commande_insufficient_stock(self):

        payload = {
            "lignes": [
                {
                    "product": self.product.id,
                    "quantity": 50
                }
            ]
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Commande.objects.count(),
            0
        )

    def test_commande_amount(self):

        payload = {
            "lignes": [
                {
                    "product": self.product.id,
                    "quantity": 2
                }
            ]
        }

        self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        commande = Commande.objects.first()

        self.assertEqual(
            commande.montant,
            500000
        )

    def test_create_commande_multiple_lines(self):

        product2 = Product.objects.create(
            category = self.categorie,
            name="Clavier",
            prix=Decimal("20000")
        )

        Inventory.objects.create(
            product=product2,
            quantity=50,
            reserved_quantity=0,
            minimum_stock=5
        )

        payload = {
            "lignes": [
                {
                    "product": self.product.id,
                    "quantity": 2
                },
                {
                    "product": product2.id,
                    "quantity": 3
                }
            ]
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            LigneCommande.objects.count(),
            2
        )

        commande = Commande.objects.first()

        expected = (
            Decimal("250000") * 2 +
            Decimal("20000") * 3
        )

        self.assertEqual(
            commande.montant,
            expected
        )

    def test_list_commandes(self):

        Commande.objects.create(
            user=self.user,
            montant=Decimal("1000")
        )

        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

    def test_retrieve_commande(self):

        commande = Commande.objects.create(
            user=self.user,
            montant=Decimal("5000")
        )

        url = reverse(
            "commande-detail",
            kwargs={
                "slug": commande.slug
            }
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["slug"],
            str(commande.slug)
        )

    def test_delete_commande(self):

        commande = Commande.objects.create(
            user=self.user,
            montant=Decimal("5000")
        )

        url = reverse(
            "commande-delete",
            kwargs={
                "slug": commande.slug
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Commande.objects.filter(
                id=commande.id
            ).exists()
        )