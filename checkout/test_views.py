from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Order, OrderLineItem


class CheckoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com', password='testpassword'
        )

    def test_checkout_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_view_post_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            name='Test Product', price=Decimal('10.00'))
        bag = {str(product.id): 2}

        self.client.session['bag'] = bag

        response = self.client.post(reverse('checkout'), {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '123456789',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'New York',
            'street_address1': '123 Main St',
            'street_address2': 'Apt 4',
            'county': 'NY',
            'client_secret': 'test_client_secret'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'checkout_success', args=[Order.objects.first().order_number]))

    def test_checkout_view_post_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('checkout'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertFormError(
            response, 'order_form', 'full_name', 'This field is required.')
        self.assertFormError(
            response, 'order_form', 'email', 'This field is required.')


class CheckoutSuccessViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com', password='testpassword'
        )

    def test_checkout_success_view(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(
            user_profile=self.user.userprofile,
            order_number='123456',
            full_name='John Doe',
            email='johndoe@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='New York',
            street_address1='123 Main St',
            street_address2='Apt 4',
            county='NY',
            grand_total=Decimal('55.00'),
        )
        response = self.client.get(reverse(
            'checkout_success', args=[order.order_number]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], order)


class CouponValidationViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.coupon = Coupon.objects.create(discount_code='TESTCODE')

    def test_coupon_validation_view_valid_coupon(self):
        response = self.client.get(
            reverse('coupon_validation'), {'coupon': 'TESTCODE'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['message'], 'Coupon is applied successfully!')
        self.coupon.refresh_from_db()
        self.assertTrue(self.coupon.used)

    def test_coupon_validation_view_invalid_coupon(self):
        response = self.client.get(reverse(
            'coupon_validation'), {'coupon': 'INVALIDCODE'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Coupon is not valid!')
        self.coupon.refresh_from_db()
        self.assertFalse(self.coupon.used)


class CacheCheckoutDataViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_cache_checkout_data_view(self):
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'test_client_secret'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')
