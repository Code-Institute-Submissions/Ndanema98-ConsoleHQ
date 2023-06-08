from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Deals
from .forms import ProductForm, ReviewForm


class AllProductsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('all_products')
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)

    def test_all_products_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_all_products_view_with_category_filter(self):
        response = self.client.get(self.url, {'categories': 'TestCategory'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'TestProduct')

    def test_all_products_view_with_search_query(self):
        response = self.client.get(self.url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'TestProduct')


class ProductsByCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory')
        self.url = reverse('products_by_category', args=[self.category.name])
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)

    def test_products_by_category_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products_by_category.html')

    def test_products_by_category_view_with_invalid_category(self):
        invalid_url = reverse('products_by_category', args=['InvalidCategory'])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)
        self.url = reverse('product_detail', args=[self.product.id])

    def test_product_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_detail_view_with_invalid_product_id(self):
        invalid_url = reverse('product_detail', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class AddProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_product')
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_add_product_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_add_product_view_with_invalid_form(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')


class EditProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)
        self.url = reverse('edit_product', args=[self.product.id])
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_edit_product_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_edit_product_view_with_invalid_product_id(self):
        invalid_url = reverse('edit_product', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_edit_product_view_with_invalid_form(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')


class DeleteProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)
        self.url = reverse('delete_product', args=[self.product.id])
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')

    def test_delete_product_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete_product_view_with_invalid_product_id(self):
        invalid_url = reverse('delete_product', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class CreateReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory')
        self.product = Product.objects.create(
            name='TestProduct',
            description='Test description',
            price=10.00,
        )
        self.product.categories.add(self.category)
        self.url = reverse('create_review', args=[self.product.id])
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_create_review_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_form.html')

    def test_create_review_view_with_invalid_product_id(self):
        invalid_url = reverse('create_review', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class NewsletterSignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('newsletter_signup')
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')

    def test_newsletter_signup_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsletter_signup.html')

    def test_newsletter_signup_view_post(self):
        response = self.client.post(self.url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter_success'))

    def test_newsletter_signup_view_post_existing_subscription(self):
        subscription = NewsletterSubscription.objects.create(user=self.user, subscribed=True)
        response = self.client.post(self.url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter_success'))
        subscription.refresh_from_db()
        self.assertTrue(subscription.subscribed)
