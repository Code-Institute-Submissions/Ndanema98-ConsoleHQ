from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class ModelsTestCase(TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(user=user)
        
        self.assertEqual(profile.user, user)
        self.assertEqual(str(profile), user.username)

    def test_create_or_update_user_profile_signal(self):
        user = User.objects.create(username='testuser')
        self.assertTrue(hasattr(user, 'userprofile'))  # Check if userprofile attribute exists

        user.username = 'updateduser'
        user.save()
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), 'updateduser')

