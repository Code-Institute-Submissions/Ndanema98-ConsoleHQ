from django.test import TestCase
from .forms import UserProfileForm


class FormsTestCase(TestCase):
    def test_user_profile_form(self):
        form = UserProfileForm()
        self.assertFalse(form.is_bound)  # Check if the form is unbound by default

        form_data = {
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': 'Test Address 1',
            'default_street_address2': 'Test Address 2',
            'default_county': 'Test County',
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_bound)  # Check if the form is bound after providing data

        self.assertTrue(form.is_valid())  # Check if the form is valid
        self.assertEqual(form.cleaned_data['default_phone_number'], '1234567890')  # Check cleaned data

        form_empty_data = {
            'default_phone_number': '',
            'default_postcode': '',
            'default_town_or_city': '',
            'default_street_address1': '',
            'default_street_address2': '',
            'default_county': '',
        }
        form = UserProfileForm(data=form_empty_data)
        self.assertFalse(form.is_valid())  # Check if the form is invalid when required fields are empty

        self.assertIn('default_phone_number', form.errors)  # Check for specific form errors

