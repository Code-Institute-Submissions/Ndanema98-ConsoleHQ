from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import ProductForm, ReviewForm, NewsletterSignupForm


class ProductFormTest(TestCase):

    def test_product_form_valid(self):
        form = ProductForm(data={
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': 9.99,
        }, files={'image': SimpleUploadedFile(
            'test_image.jpg', b'file_content')})
        self.assertTrue(form.is_valid())

    def test_product_form_invalid(self):
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class ReviewFormTest(TestCase):

    def test_review_form_valid(self):
        form = ReviewForm(data={
            'name': 'John Doe',
            'content': 'This is a great product!',
        })
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        form = ReviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class NewsletterSignupFormTest(TestCase):

    def test_newsletter_signup_form_valid(self):
        form = NewsletterSignupForm(data={
            'email': 'test@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_newsletter_signup_form_invalid(self):
        form = NewsletterSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Expecting error for 'email'
