from django.core import mail
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Coupon
from .utils import send_subscription_email, generate_coupon_code


class UtilsTestCase(TestCase):
    def test_send_subscription_email(self):
        user = User.objects.create_user(
            username='testuser', email='test@example.com')
        send_subscription_email(user)

        self.assertEqual(len(mail.outbox), 1)  # Check if an email is sent
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Subscribed to Newsletter")
        self.assertEqual(
            email.body, f"You are successfully subscribed to the newletter. You can use {Coupon.objects.first().discount_code} for the available 20% discount.")
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to, [user.email])

    def test_generate_coupon_code(self):
        coupon_code = generate_coupon_code()

        self.assertEqual(len(coupon_code), 8)  # Check if the generated code has a length of 8

        # Check if the generated code contains only uppercase letters and digits
        self.assertTrue(all(
            char.isupper() or char.isdigit() for char in coupon_code))
