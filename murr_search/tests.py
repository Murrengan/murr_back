from rest_framework.test import APITestCase

from murr_card.models import MurrCard
from murren.models import Murren


class SearchMurrenViewTests(APITestCase):

    def setUp(self) -> None:
        self.api = r'/api/search/murren/?search='
        self.test_user = Murren.objects.create_user(
            username='murren',
            email='admin@murrengan.ru',
        )

    def tearDown(self) -> None:
        del self.api
        del self.test_user

    def test_search_murren_username(self) -> None:
        search_text = 'murr'
        response = self.client.get(f'{self.api}{search_text}')

        self.assertEqual(response.status_code, 200)
        murren = response.data['results'][0]
        self.assertEqual(murren['username'], 'murren')
        self.assertEqual(murren['email'], 'admin@murrengan.ru')


class SearchMurrCardViewTests(APITestCase):

    def setUp(self) -> None:
        self.api = r'/api/search/murr_card/?search='
        self.test_user = Murren.objects.create(
            username='murren',
            email='admin@murrengan.ru',
        )
        self.test_card = MurrCard.objects.create(
            title='murr card',
            content='murren test card',
            owner=self.test_user,
        )

    def tearDown(self) -> None:
        del self.api
        del self.test_user

    def test_search_murren_name(self) -> None:
        search_text = 'card'
        response = self.client.get(f'{self.api}{search_text}')

        self.assertEqual(response.status_code, 200)
        murr_card = response.data['results'][0]
        self.assertEqual(murr_card['title'], 'murr card')
        self.assertEqual(murr_card['content'], 'murren test card')
        self.assertEqual(murr_card['owner_name'], 'murren')
