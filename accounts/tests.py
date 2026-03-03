from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.


class UserManagersTests(TestCase):
    def test_create_user(self):
        # we setup the User class here because we want to use it to mimick users
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


class SignUpTests(TestCase):
    def test_signup_exist_at_specific_location(self):
        response = self.client.get("/accounts/signup/")
        # this is us navigating to the status_code.
        self.assertEqual(response.status_code, 200)

    def test_signup_by_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertContains(response, "Sign Up")

    def test_signup_page(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "test_user",
                "email": "example@example.com",
                "age": 25,
                "password1": "secret212",
                "password2": "secret212",
            },
        )
        # should return a redirect 302 if succesful
        # returns a 200 if there is a form error
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "test_user")
        self.assertEqual(get_user_model().objects.all()[0].email, "example@example.com")
        self.assertEqual(get_user_model().objects.all()[0].age, 25)
