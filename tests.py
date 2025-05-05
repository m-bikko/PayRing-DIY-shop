#!/usr/bin/env python3
"""
PayRing Application Tests
This script tests various functionality of the PayRing application.
"""

import unittest
import os
import tempfile
from flask import Flask
from app import create_app
from app.models.database import db
from app.models.user import User
from app.models.product import KitType, RingType, RingSize
from app.models.order import Order, OrderItem

class PayRingTestCase(unittest.TestCase):
    """Test case for the PayRing application."""

    def setUp(self):
        """Set up a test environment."""
        self.db_fd, self.db_file = tempfile.mkstemp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_file}'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test data
            self._create_test_data()

    def tearDown(self):
        """Tear down the test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_file)

    def _create_test_data(self):
        """Create test data for the test cases."""
        # Create admin user
        admin = User(username='testadmin')
        admin.set_password('testpassword')
        db.session.add(admin)
        
        # Create kit types
        info_ring = KitType(
            name='InfoRing',
            description='Info Ring kit for sharing contact info or links',
            price=49.99,
            image_url='https://example.com/images/infoRing.jpg'
        )
        access_ring = KitType(
            name='AccessRing',
            description='Access Ring kit for secure access control',
            price=59.99,
            image_url='https://example.com/images/accessRing.jpg'
        )
        pay_ring = KitType(
            name='PayRing',
            description='Pay Ring kit for contactless payments',
            price=79.99,
            image_url='https://example.com/images/payRing.jpg'
        )
        db.session.add_all([info_ring, access_ring, pay_ring])
        
        # Create ring types
        metal_ring = RingType(
            name='Metal',
            image_url='https://example.com/images/metal-ring.jpg'
        )
        silicone_ring = RingType(
            name='Silicone',
            image_url='https://example.com/images/silicone-ring.jpg'
        )
        db.session.add_all([metal_ring, silicone_ring])
        
        # Create ring sizes
        sizes = [
            RingSize(size='US5'),
            RingSize(size='US6'),
            RingSize(size='US7'),
            RingSize(size='US8'),
            RingSize(size='US9')
        ]
        db.session.add_all(sizes)
        
        # Create a test order
        order = Order(
            customer_name='Test Customer',
            customer_email='test@example.com',
            customer_phone='123-456-7890',
            shipping_address='123 Test St, Test City, TC 12345',
            total_amount=114.97,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # To get order ID
        
        # Create order items
        order_item = OrderItem(
            order_id=order.id,
            kit_type_id=1,  # InfoRing
            ring_type_id=1,  # Metal
            ring_size_id=3,  # US7
            quantity=1,
            price=49.99
        )
        db.session.add(order_item)
        
        # Commit changes
        db.session.commit()
    
    def test_landing_page(self):
        """Test that the landing page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PayRing', response.data)
    
    def test_shop_page(self):
        """Test that the shop page loads correctly and shows products."""
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'InfoRing', response.data)
        self.assertIn(b'AccessRing', response.data)
        self.assertIn(b'PayRing', response.data)
    
    def test_product_detail_page(self):
        """Test that a product detail page loads correctly."""
        response = self.client.get('/shop/kit/1')  # InfoRing
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'InfoRing', response.data)
        self.assertIn(b'49.99', response.data)
    
    def test_admin_login_page(self):
        """Test that the admin login page loads correctly."""
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Login', response.data)
    
    def test_admin_login(self):
        """Test admin login functionality."""
        response = self.client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_create_order(self):
        """Test creating a new order."""
        order_data = {
            'customerName': 'New Customer',
            'customerEmail': 'new@example.com',
            'customerPhone': '987-654-3210',
            'shippingAddress': '456 New St, New City, NC 54321',
            'items': [{
                'kitTypeId': 2,  # AccessRing
                'ringTypeId': 2,  # Silicone
                'ringSizeId': 4,  # US8
                'quantity': 1
            }]
        }
        response = self.client.post('/shop/order', 
                                   json=order_data, 
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertTrue('orderId' in response_data)
    
    def test_admin_orders_page(self):
        """Test that the admin orders page loads correctly after login."""
        # First login
        self.client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'testpassword'
        })
        
        # Then access orders page
        response = self.client.get('/admin/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Customer', response.data)
        self.assertIn(b'pending', response.data)

if __name__ == '__main__':
    unittest.main()