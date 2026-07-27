from django.test import TestCase
from .models import Inventory
from django.urls import reverse
from categorie.models import Category
from product.models import Product
from mouvement_stock.models import MouvementStock

class TestInventory(TestCase):
    def setUp(self):
        self.categorie = Category.objects.create(name='test_cate')
        self.product = Product.objects.create(category=self.categorie,name='produit_test',prix=123)
        self.product1 = Product.objects.create(category=self.categorie,name='produit',prix=139)
        self.inventory = Inventory.objects.create(product=self.product, quantity=123, minimum_stock=4)
    
    def testInstance(self):
        self.assertIsInstance(self.inventory, Inventory)
    
    
    def test_if_exist(self):
        inv = Product.objects.get(id=1)
        self.assertTrue(inv)


    def test_create(self):
        url_create = 'inventory-create'
        data = {
            'product':self.product1.id,
            'quantity': 345,
            'minimum_stock':12
        }
        result = self.client.post(reverse(url_create), data, format='json')
        self.assertEqual(result.status_code, 201)

        mouv = MouvementStock.objects.get(id=1)
        self.assertTrue(mouv)
        self.assertEqual(mouv.quantity, 345)

    def test_delete(self):
        url_delete = 'inventory-delete'
        url_create = 'inventory-create'
        url_delete_mouv = 'delete-mouvementStock'
        data = {
            'product':self.product1.id,
            'quantity': 345,
            'minimum_stock':12
        }
        result = self.client.post(reverse(url_create), data, format='json')
        self.assertEqual(result.status_code, 201)
        slug = result.json()['slug']

        mouv = MouvementStock.objects.get(id=1)
        self.assertTrue(mouv)
        self.assertEqual(mouv.quantity, 345)

        mouv_slug = mouv.slug

        result_del = self.client.delete(reverse(url_delete_mouv, args=[mouv_slug]))
        self.assertEqual(result_del.status_code, 204)


        result_delete_inventory = self.client.delete(reverse(url_delete, args=[slug]))
        self.assertEqual(result_delete_inventory.status_code, 204)

