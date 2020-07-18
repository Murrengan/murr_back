import pytest
from channels.db import database_sync_to_async
from channels.testing.websocket import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import Client

from murr_back.routing import application


@database_sync_to_async
def create_murren(username, email, password):
    murren = get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return murren


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_murr_chat():
    client_1 = Client()
    murren_1 = await create_murren('test1', 'test1@test.com', 'password1')
    murren_2 = await create_murren('test2', 'test2@test.com', 'password2')
    client_1.force_login(user=murren_1)
    communicator_1 = WebsocketCommunicator(application=application,
                                           path='/ws/murr_chat/lobby/',
                                           headers=[('pytest', murren_1.id)])

    connected, _ = await communicator_1.connect()
    assert connected

    await communicator_1.send_json_to({"data": {"murr_chat_name": "___________"}, "gan": "create_murr_chat"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'create_murr_chat'
    assert message['data']['murr_chat_name'] == '___________'
    murr_chat_url = message['data']['link']

    await communicator_1.send_json_to({"data": {}, "gan": "get_murren_chats_list"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'get_murren_chats_list'
    assert len(message['data']) == 1

    await communicator_1.send_json_to({"data": {}, "gan": "get_murren_list"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'get_murren_list'
    assert len(message['data']) == 1

    await communicator_1.disconnect()

    communicator_1 = WebsocketCommunicator(application=application,
                                           path=murr_chat_url,
                                           headers=[('pytest', murren_1.id)])
    connected, _ = await communicator_1.connect()
    assert connected

    communicator_2 = WebsocketCommunicator(application=application,
                                           path='/ws/murr_chat/lobby/',
                                           headers=[('pytest', murren_2.id)])
    connected2, _ = await communicator_2.connect()
    assert connected2

    await communicator_1.send_json_to({"data": {"murren_id": murren_2.id}, "gan": "add_murr_chat_member"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'add_murr_chat_member'
    assert len(message['data']) == 2

    message = await communicator_2.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'new_murr_chat_member'

    await communicator_1.send_json_to({"data": {"message": "___________"}, "gan": "send_message"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'send_message'
    assert message['data']['message'] == '___________'

    message = await communicator_2.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'new_murr_chat_message'

    await communicator_2.disconnect()
    communicator_2 = WebsocketCommunicator(application=application,
                                           path=murr_chat_url,
                                           headers=[('pytest', murren_2.id)])
    connected2, _ = await communicator_2.connect()
    assert connected2

    await communicator_1.send_json_to({"data": {"message": "___________2"}, "gan": "send_message"})
    message = await communicator_1.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'send_message'
    assert message['data']['message'] == '___________2'

    message = await communicator_2.receive_json_from()
    assert message['status'] == 'ok'
    assert message['gan'] == 'send_message'
    assert message['data']['message'] == '___________2'

    await communicator_1.disconnect()
    await communicator_2.disconnect()
