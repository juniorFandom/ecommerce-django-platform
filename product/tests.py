from django.test import TestCase

# Create your tests here.
class ProductAPITestCase(TestCase):
    def test_product_list(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_product_create(self):
        data = {
            "name": "Test Product",
            "prix": 9.99,
            "is_active": True
        }
        response = self.client.post('/products/create/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

    def test_product_update(self):
        # First, create a product to update
        create_data = {
            "name": "Product to Update",
            "prix": 19.99,
            "is_active": True
        }
        create_response = self.client.post('/products/create/', create_data, content_type='application/json')
        product_id = create_response.json()['id']
        
        update_data = {
            "name": "Updated Product",
            "prix": 29.99,
            "is_active": False
        }
        response = self.client.put(f'/products/{product_id}/update/', update_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Updated Product")

    def test_product_delete(self):
        # First, create a product to delete
        create_data = {
            "name": "Product to Delete",
            "prix": 15.99,
            "is_active": True
        }
        create_response = self.client.post('/products/create/', create_data, content_type='application/json')
        product_id = create_response.json()['id']
        
        response = self.client.delete(f'/products/{product_id}/delete/')
        self.assertEqual(response.status_code, 204)