from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Order, OrderLineItem
from products.models import Product


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user_profile=self.user.userprofile,
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='New York',
            street_address1='123 Main St',
            street_address2='Apt 4',
            county='NY',
            delivery_cost=Decimal('5.00'),
            order_total=Decimal('50.00'),
            grand_total=Decimal('55.00'),
            original_bag='{"1": 2}',
            stripe_pid='stripepid123'
        )

        self.assertEqual(order.user_profile, self.user.userprofile)
        self.assertEqual(order.full_name, 'John Doe')
        self.assertEqual(order.email, 'johndoe@example.com')
        self.assertEqual(order.phone_number, '123456789')
        self.assertEqual(order.country, 'US')
        self.assertEqual(order.postcode, '12345')
        self.assertEqual(order.town_or_city, 'New York')
        self.assertEqual(order.street_address1, '123 Main St')
        self.assertEqual(order.street_address2, 'Apt 4')
        self.assertEqual(order.county, 'NY')
        self.assertEqual(order.delivery_cost, Decimal('5.00'))
        self.assertEqual(order.order_total, Decimal('50.00'))
        self.assertEqual(order.grand_total, Decimal('55.00'))
        self.assertEqual(order.original_bag, '{"1": 2}')
        self.assertEqual(order.stripe_pid, 'stripepid123')

    def test_order_number_generation(self):
        order = Order.objects.create(user_profile=self.user.userprofile)
        self.assertIsNotNone(order.order_number)

    def test_update_total(self):
        order = Order.objects.create(user_profile=self.user.userprofile)
        product = Product.objects.create(name='Test Product', price=Decimal('10.00'))
        line_item = OrderLineItem.objects.create(order=order, product=product, quantity=2)

        order.update_total()
        self.assertEqual(order.order_total, Decimal('20.00'))
        self.assertEqual(order.delivery_cost, Decimal('0.00'))
        self.assertEqual(order.grand_total, Decimal('20.00'))


class OrderLineItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )
        self.order = Order.objects.create(user_profile=self.user.userprofile)
        self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'))

    def test_line_item_creation(self):
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            lineitem_total=Decimal('20.00')
        )

        self.assertEqual(line_item.order, self.order)
        self.assertEqual(line_item.product, self.product)
        self.assertEqual(line_item.quantity, 2)
        self.assertEqual(line_item.lineitem_total, Decimal('20.00'))
