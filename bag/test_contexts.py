from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from products.models import Product, NewsletterSubscription
from .contexts import bag_contents


class BagContentsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(name='Test Product', price=10)
        self.discounted_product = Product.objects.create(
            name='Discounted Product', price=20, discount_price=15)
        self.user = AnonymousUser()

    def test_bag_contents(self):
        request = self.factory.get('/')
        request.session = {'bag': {str(
            self.product.pk): 2, str(self.discounted_product.pk): 3}}
        context = bag_contents(request)

        self.assertEqual(
            context['bag_items'][0]['item_id'], str(self.product.pk))
        self.assertEqual(context['bag_items'][0]['quantity'], 2)
        self.assertEqual(context['bag_items'][0]['product'], self.product)

        self.assertEqual(context['bag_items'][1]['item_id'], str(
            self.discounted_product.pk))
        self.assertEqual(context['bag_items'][1]['quantity'], 3)
        self.assertEqual(
            context['bag_items'][1]['product'], self.discounted_product)

        self.assertEqual(context['total'], 95)  # (2 * 10) + (3 * 15)
        self.assertEqual(context['product_count'], 5)  # 2 + 3

        self.assertEqual(context['delivery'], 0)
        self.assertEqual(context['free_delivery_delta'], Decimal(
            settings.FREE_DELIVERY_THRESHOLD) - 95)
        self.assertEqual(
            context['free_delivery_threshold'], settings.FREE_DELIVERY_THRESHOLD)
        self.assertEqual(context['grand_total'], 95)

    def test_bag_contents_with_discount(self):
        request = self.factory.get('/')
        request.session = {'bag': {str(self.discounted_product.pk): 1}}
        request.user = self.user
        subscription = NewsletterSubscription.objects.create(
            user=self.user, subscribed=True, coupon_used=False)
        context = bag_contents(request)

        self.assertEqual(context['total'], 15)  # 1 * 15 (discounted price)
        self.assertEqual(context['grand_total'], 12)  # 15 - (15 * 0.2) (discount applied)