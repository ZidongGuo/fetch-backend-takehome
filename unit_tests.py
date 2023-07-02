import unittest
from app import app
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()


    def test_target_receipt(self):
        with open('./examples/target-receipt.json') as f:
            data=json.load(f)
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        id= response.json['id']
        point_response =self.app.get('/receipts/{}/points'.format(id), json=data)
        self.assertEqual(point_response.status_code, 200)
        self.assertIn('points', point_response.json)
        correct_points=28    
        self.assertEqual(point_response.json['points'], correct_points)

    
    def test_MM_receipt(self):
        f = open('./examples/M&M-receipt.json')
        data=json.load(f)
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        id= response.json['id']
        point_response =self.app.get('/receipts/{}/points'.format(id), json=data)
        self.assertEqual(point_response.status_code, 200)
        self.assertIn('points', point_response.json)
        correct_points=109    
        self.assertEqual(point_response.json['points'], correct_points)


    def test_simple_receipt(self):
        with open('./examples/simple-receipt.json') as f:
            data=json.load(f)
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        id= response.json['id']
        point_response =self.app.get('/receipts/{}/points'.format(id), json=data)
        self.assertEqual(point_response.status_code, 200)
        self.assertIn('points', point_response.json)
        correct_points=31    
        self.assertEqual(point_response.json['points'], correct_points)


    def test_morning_receipt(self):
        with open('./examples/morning-receipt.json') as f:
            data=json.load(f)
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        id= response.json['id']
        point_response =self.app.get('/receipts/{}/points'.format(id), json=data)
        self.assertEqual(point_response.status_code, 200)
        self.assertIn('points', point_response.json)
        correct_points=15   
        self.assertEqual(point_response.json['points'], correct_points)


    def test_missing_post_parameter(self):
        data ={
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 400)


    def test_empty_post_parameter(self):
        data ={
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "item2", "price":""}
            ]
        }
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 400)


    def test_wrong_post_parameter_type(self):
        data ={
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": 1.25,
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "item2", "price":100}
            ]
        }
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 400)

    def test_irregular_parameter_input(self):
        data ={
            "retailer": "Target",
            "purchaseDate": "2022-99-99",
            "purchaseTime": "99:99",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "item2", "price":""}
            ]
        }
        response = self.app.post('/receipts/process', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_points_invalid(self):
        receipt_id = 'invalid_receipt_id'
        response = self.app.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)



if __name__ == '__main__':
    unittest.main()
    print("Passed all unit tests")