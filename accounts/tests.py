from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="secret",
            age=39,
        )
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("secret"))
        self.assertEqual(user.age, 39)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        User = get_user_model()
        s_user = User.objects.create_superuser(
            username="test_user",
            email="test@example.com",
            password="secret",
            age=39,
        )
        self.assertEqual(s_user.username, "test_user")
        self.assertEqual(s_user.email, "test@example.com")
        self.assertTrue(s_user.check_password("secret"))
        self.assertEqual(s_user.age, 39)

        self.assertTrue(s_user.is_staff)
        self.assertTrue(s_user.is_superuser)
        self.assertTrue(s_user.is_active)
