from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Product, Category, Review, Deals, NewsletterSubscription, Coupon
)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='TestCategory', friendly_name='Test Friendly Name'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'TestCategory')

    def test_category_get_friendly_name(self):
        self.assertEqual(
            self.category.get_friendly_name(), 'Test Friendly Name')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'TestProduct')

    def test_product_get_discounted_price_without_deal(self):
        self.assertIsNone(self.product.get_discounted_price())

    def test_product_get_discounted_price_with_deal(self):
        deals = Deals.objects.create(
            category=self.category, discount_percentage=20.0)
        self.assertEqual(self.product.get_discounted_price(), 8.00)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct', description='Test description', price=10.00)
        self.product.categories.add(self.category)
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.review = Review.objects.create(
            product=self.product,
            name='Test Review',
            author=self.user,
            content='Test content',
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), 'Review for TestProduct')


class DealsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')
        self.deals = Deals.objects.create(
            category=self.category, discount_percentage=20.0)

    def test_deals_str(self):
        self.assertEqual(str(self.deals), 'Deals for TestCategory')


class NewsletterSubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.subscription = NewsletterSubscription.objects.create(
            user=self.user)

    def test_newsletter_subscription_str(self):
        self.assertEqual(str(self.subscription), 'testuser')


class CouponModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.coupon = Coupon.objects.create(
            user=self.user, discount_code='TESTCODE')

    def test_coupon_str(self):
        self.assertEqual(str(self.coupon), 'TESTCODE')

    def test_generate_discount_code(self):
        discount_code = Coupon.generate_discount_code()
        self.assertEqual(len(discount_code), 8)
        self.assertTrue(discount_code.isalnum())

    def test_create_coupon(self):
        coupon = Coupon.create_coupon(user=self.user)
        self.assertEqual(coupon.user, self.user)
        self.assertEqual(len(coupon.discount_code), 8)
        self.assertFalse(coupon.used)
