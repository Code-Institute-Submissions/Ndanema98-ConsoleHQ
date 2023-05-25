import random
import string

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    categories = models.ManyToManyField(Category)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80, default="Anonymous")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products_reviews",
    )
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Review for {self.product.name}'


class Deals(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"Deals for {self.category.name}"


class NewsletterSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=20, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.discount_code

    @staticmethod
    def generate_discount_code():
        code_length = 8
        characters = string.ascii_uppercase + string.digits
        discount_code = ''.join(random.choice(characters) for _ in range(code_length))
        return discount_code

    @classmethod
    def create_coupon(cls, user):
        discount_code = cls.generate_discount_code()
        coupon = cls(user=user, discount_code=discount_code)
        coupon.save()
        return coupon
