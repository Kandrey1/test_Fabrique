import pytest
from django.urls import reverse

from mailing.models import Client


@pytest.mark.django_db
def test_mailing_api_client_add(api_client, data_client_1, data_client_2):
    """
    Тестирование добавления клиента по API.
    (POST запрос)
    """
    assert Client.objects.count() == 0

    url = reverse('client_add')
    response = api_client.post(url, data_client_1, format='json')

    assert response.status_code == 201
    assert Client.objects.count() == 1
    assert Client.objects.first().phone == 79876543210
    assert Client.objects.first().code_phone == 'mts'
    assert Client.objects.first().timezone == "Europe/Moscow"

    response = api_client.post(url, data_client_2)

    assert response.status_code == 201
    assert Client.objects.count() == 2
    assert Client.objects.last().phone == 77776543219
    assert Client.objects.last().code_phone == 'tele2'


@pytest.mark.django_db
def test_mailing_api_client_update(api_client, client_1, data_client_2):
    """
    Тестирование обновления данных клиента по API.
    (PUT запрос)
    """
    assert Client.objects.count() == 0

    client_1.save()

    assert Client.objects.count() == 1
    assert Client.objects.first().phone == 79876543210
    assert Client.objects.first().timezone == "Europe/Moscow"

    url = reverse('client_up', kwargs={'pk': 1})
    response = api_client.put(url, data_client_2, format='json')

    assert response.status_code == 200
    assert Client.objects.count() == 1
    assert Client.objects.first().phone == 77776543219
    assert Client.objects.first().timezone == "Europe/Vatican"


@pytest.mark.django_db
def test_mailing_api_client_delete(api_client, client_1, client_2):
    """
    Тестирование удаление клиента из БД по API.
    (DELETE запрос)
    """
    assert Client.objects.count() == 0

    client_1.save()

    assert Client.objects.count() == 1
    assert Client.objects.first().phone == 79876543210
    assert Client.objects.first().timezone == "Europe/Moscow"

    client_2.save()

    assert Client.objects.count() == 2
    assert Client.objects.last().phone == 77776543219
    assert Client.objects.last().timezone == "Europe/Vatican"

    # проверка доступа без токена
    url = reverse('client_del', kwargs={'pk': 2})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Client.objects.count() == 1
    assert Client.objects.last().phone == 79876543210
    assert Client.objects.first().timezone == "Europe/Moscow"

    url = reverse('client_del', kwargs={'pk': 1})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Client.objects.count() == 0
