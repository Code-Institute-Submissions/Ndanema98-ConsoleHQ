from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user)
        self.order = Order.objects.create(
            order_number='123456', user=self.user, total=10)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile')
        form_data = {
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': 'Test Address 1',
            'default_street_address2': 'Test Address 2',
            'default_county': 'Test County',
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserProfile.objects.filter(
            user=self.user,
            default_phone_number='1234567890',
            default_postcode='12345',
            default_town_or_city='Test City',
            default_street_address1='Test Address 1',
            default_street_address2='Test Address 2',
            default_county='Test County',
        ).exists())
        self.assertFormSuccess(response, 'Profile updated successfully!')

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('order_history', args=['123456'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], self.order)

