from django.test import TestCase
from django.contrib.auth import get_user_model

AppUser = get_user_model()

class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = AppUser.objects.create_user(
            email="profile@test.com",
            password="123456"
        )

    def test_profile_auto_created(self):
        user = AppUser.objects.create_user(
            email="auto@test.com",
            password="123"
        )
        self.assertTrue(hasattr(user, 'profile'))

    def test_profile_str(self):
        profile = self.user.profile
        expected = f"{self.user.get_full_name()}'s profile"
        self.assertEqual(str(profile), expected)
