from django.core.mail import send_mail
from django.conf import settings
import random
import string
from products.models import Coupon


def send_subscription_email(user):
    coupon = Coupon.objects.create(
        user=user,
        discount_code=generate_coupon_code(),
        # discount_amount = 0
    )
    subject = "Subscribed to Newsletter"
    body = f"You are successfully subscribed to the newletter.You can use {coupon.discount_code} for the avaliable 20% discount."
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    ) 


def generate_coupon_code(length=8):
    characters = string.ascii_uppercase + string.digits
    coupon_code = ''.join(random.choice(characters) for _ in range(length))
    return coupon_code
