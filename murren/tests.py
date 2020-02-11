from django.contrib.auth import get_user_model
from django.test import TestCase


class MurrenTests(TestCase):

    def test_create_user(self):
        Murren = get_user_model()
        user = Murren.objects.create_user(
            username='murren',
            email='murren@email.com',
            password='murren_pass_123'
        )
        self.assertEqual(user.username, 'murren')
        self.assertEqual(user.email, 'murren@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):

        Murren = get_user_model()
        admin_user = Murren.objects.create_superuser(
            username='admin_murren',
            email='admin_murren@email.com',
            password='admin_murren_pass'
        )
        self.assertEqual(admin_user.username, 'admin_murren')
        self.assertEqual(admin_user.email, 'admin_murren@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
