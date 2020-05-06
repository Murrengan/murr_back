import json


from django.contrib.auth import get_user_model
from django.core import mail
from django.test import modify_settings
from django.urls import reverse
from rest_framework.test import force_authenticate
from django.test.client import encode_multipart, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from murr_card.models import MurrCard


Murren = get_user_model()

"""Что тестить?
1. корректность переданных данных.
2. проверка на удаление от не владельца.
3. зарегать текущего пользователя.
Это две разные функции? или два разных теста?
request.user.id
"""


class MurrTests(APITestCase):
    def setUp(self):
        user1 = Murren.objects.create_user(username='dan',
                                           password='12345',
                                           email='integrity@mail.com')
        user1.save()
        user2 = Murren.objects.create_user(username='Frost',
                                           password='1q2w3e',
                                           email='integrity1@mail.com')
        user2.save()
        self.one_murr = MurrCard.objects.create(
            title=1,
            content="hello, it's me",
            owner=user1
        )
        self.two_murr = MurrCard.objects.create(
            title=2,
            content="Halo, dat's not me",
            owner=user2
        )

    def test_detail_murr_db(self):
        murr = MurrCard.objects.get(id=self.one_murr.title)
        print(murr)
        self.assertEqual(int(murr.title), 1)



