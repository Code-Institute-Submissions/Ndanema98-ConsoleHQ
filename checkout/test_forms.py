from django.test import TestCase
from .forms import OrderForm


class FormsTestCase(TestCase):
    def test_order_form(self):
        form_data = {
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': 'Test Address 1',
            'street_address2': 'Test Address 2',
            'county': 'Test County',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_required_fields(self):
        form_data = {}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)
        self.assertIn('full_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('phone_number', form.errors)
        self.assertIn('postcode', form.errors)
        self.assertIn('town_or_city', form.errors)
        self.assertIn('street_address1', form.errors)
        self.assertIn('county', form.errors)
