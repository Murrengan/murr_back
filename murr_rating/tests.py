import json

from rest_framework.test import APITestCase

from murr_card.models import MurrCard
from murren.models import Murren
from .models import Rating


class RatingTests(APITestCase):

    def setUp(self):
        self.api = r'/api/murr_card'
        self.test_user = Murren.objects.create(username='test_rating', email='admin@murrengan.ru')
        self.test_card = MurrCard.objects.create(title='test_rating', content='', owner=self.test_user)

    def get_rating(self):
        return Rating.objects.filter(murren=self.test_user, object_id=self.test_card.id, object_type='MurrCard').first()

    def test_create_rating(self):
        like_card_url = f'{self.api}/{self.test_card.id}/like/'
        dislike_card_url = f'{self.api}/{self.test_card.id}/dislike/'

        response = self.client.post(like_card_url)
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.test_user)

        response = self.client.post(like_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating().rating_type, 'Like')

        response = self.client.post(like_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating(), None)

        response = self.client.post(dislike_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating().rating_type, 'Dislike')

        response = self.client.post(dislike_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating(), None)

        response = self.client.post(dislike_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating().rating_type, 'Dislike')

        response = self.client.post(like_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating().rating_type, 'Like')

        self.assertEqual(self.get_rating().rating_type, 'Like')
        response = self.client.post(dislike_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating().rating_type, 'Dislike')

        response = self.client.post(dislike_card_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_rating(), None)
