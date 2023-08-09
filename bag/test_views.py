from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from products.models import Product, NewsletterSubscription
from .views import (
    view_bag,
    add_to_bag,
    adjust_bag,
    delete_item_bag,
    subscribe_to_newsletter
)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10)
        self.subscription = NewsletterSubscription.objects.create(
            user=self.user)

    def test_view_bag(self):
        request = self.factory.get(reverse('view_bag'))
        request.user = self.user
        response = view_bag(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
        self.assertEqual(response.context['newsletter'], self.subscription)

    def test_add_to_bag(self):
        request = self.factory.post(reverse(
            'add_to_bag', args=[self.product.pk]), data={
                'quantity': 2, 'redirect_url': '/'})
        request.user = self.user
        response = add_to_bag(request, self.product.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(get_messages(request)), 1)
        self.assertEqual(request.session['bag'][str(self.product.pk)], 2)

    def test_adjust_bag(self):
        request = self.factory.post(reverse(
            'adjust_bag', args=[self.product.pk]), data={'quantity': 3})
        request.user = self.user
        request.session['bag'] = {str(self.product.pk): 2}
        response = adjust_bag(request, self.product.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(get_messages(request)), 1)
        self.assertEqual(request.session['bag'][str(self.product.pk)], 3)

    def test_delete_item_bag(self):
        request = self.factory.get(reverse(
            'delete_item_bag', args=[self.product.pk]))
        request.user = self.user
        request.session['bag'] = {str(self.product.pk): 2}
        response = delete_item_bag(request, self.product.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(get_messages(request)), 1)
        self.assertNotIn(str(self.product.pk), request.session['bag'])

    def test_subscribe_to_newsletter(self):
        request = self.factory.get(reverse('subscribe_to_newsletter'))
        request.user = self.user
        response = subscribe_to_newsletter(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(
            )['message'], 'Unsubscribed to newsletter Successfully!')
        self.subscription.refresh_from_db()
        self.assertTrue(self.subscription.subscribed)
