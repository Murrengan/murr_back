from rest_framework.test import APIClient
import pytest

from murr_card.models import MurrCard


@pytest.mark.django_db
def test_murren_create_comment_for_murr(create_murren, create_murr):
    murren = create_murren
    murr = create_murr
    api = APIClient()
    api.force_authenticate(user=murren)
    data = {
        "author": murren.pk,
        "murr": murr.pk,
        "text": "Текст моего секси комментария",
    }

    murr_comment_parent = api.post('/api/murr_comments/', data, format='json')
    assert murr_comment_parent.status_code == 201
    murr_card = MurrCard.objects.get(pk=murr.pk)
    assert murr_card.owner_id == murren.pk
    assert murr_card.pk == murr.pk

    murr_comments_list = api.get(f'/api/murr_comments/{murr_card.pk}/')
    assert murr_comments_list.status_code == 200
    assert murr_comments_list.data['results'][0]['author_username'] == murren.username
    assert murr_comments_list.data['results'][0]['text'] == "Текст моего секси комментария"
    assert murr_comments_list.data['results'][0]['murr'] == murr.pk
    assert murr_comments_list.data['results'][0]['id'] == murr.pk
    api.post('/api/murr_comments/', data, format='json')

    response = api.get(f'/api/murr_comments/')
    assert response.status_code == 200
    assert response.data['count'] == 2


@pytest.mark.django_db
def test_murren_create_comment_for_comment(create_murren, create_murr):
    murren = create_murren
    murr = create_murr
    api = APIClient()
    api.force_authenticate(user=murren)
    data = {
        "author": murren.pk,
        "murr": murr.pk,
        "text": "Текст моего секси комментария",
    }
    murr_comment_parent = api.post('/api/murr_comments/', data, format='json')
    assert murr_comment_parent.status_code == 201
    murr_card = MurrCard.objects.get(pk=murr.pk)
    assert murr_card.owner_id == murren.pk
    assert murr_card.pk == murr.pk
    murr_comments_list = api.get(f'/api/murr_comments/{murr_card.pk}/')
    data = {
        "author": murren.pk,
        "murr": murr.pk,
        "text": "Children text comment",
        "parent": murr_comments_list.data['results'][0]['murr']
    }
    api.post('/api/murr_comments/', data, format='json')
    murr_comments_list = api.get(f'/api/murr_comments/{murr_card.pk}/')

    assert data['text'] == murr_comments_list.data['results'][0]['children'][0]['text']


@pytest.mark.django_db
def test_create_comment_when_murren_is_banned(create_murren_is_banned, create_murr):
    murren = create_murren_is_banned
    murr = create_murr
    api = APIClient()
    api.force_authenticate(user=murren)
    data = {
        "author": murren.pk,
        "murr": murr.pk,
        "text": "Текст моего секси комментария",
    }
    murr_comment_parent = api.post('/api/murr_comments/', data, format='json')
    assert murr_comment_parent.status_code == 403
