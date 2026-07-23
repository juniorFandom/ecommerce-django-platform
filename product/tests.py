from django.test import TestCase
from django.urls import reverse


class ProductAPITestCase(TestCase):

    def test_product_list(self):
        url = reverse('product-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


    def test_product_create(self):
        url = reverse('product-create')

        data = {
            "name": "Test Product",
            "prix": 9.99,
            "is_active": True
        }

        response = self.client.post(
            url,
            data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())


    def test_product_update(self):

        create_url = reverse('product-create')

        create_data = {
            "name": "Product to Update",
            "prix": 19.99,
            "is_active": True
        }

        create_response = self.client.post(
            create_url,
            create_data,
            content_type='application/json'
        )

        self.assertEqual(create_response.status_code, 201)

        product_slug = create_response.json()['slug']

        update_url = reverse(
            'product-update',
            kwargs={'slug': product_slug}
        )

        update_data = {
            "name": "Updated Product",
            "prix": 29.99,
            "is_active": False
        }

        response = self.client.put(
            update_url,
            update_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['name'],
            "Updated Product"
        )


    def test_product_delete(self):

        create_url = reverse('product-create')

        create_data = {
            "name": "Product to Delete",
            "prix": 15.99,
            "is_active": True
        }

        create_response = self.client.post(
            create_url,
            create_data,
            content_type='application/json'
        )

        self.assertEqual(create_response.status_code, 201)

        product_slug = create_response.json()['slug']

        delete_url = reverse(
            'product-delete',
            kwargs={'slug': product_slug}
        )

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 204)