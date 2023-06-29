import pytest
from django.urls import reverse

from mailing.models import Mailing


@pytest.mark.django_db
def test_mailing_api_mailing_add(api_client, data_mailing_1, data_mailing_2):
    """
    Тестирование добавления рассылки по API.
    (POST запрос)
    """
    assert Mailing.objects.count() == 0

    url = reverse('mailing_add')
    response = api_client.post(url, data_mailing_1)

    assert response.status_code == 201
    assert Mailing.objects.count() == 1
    assert Mailing.objects.first().message == 'message one'
    assert Mailing.objects.first().filter_client == "mts, filter one"

    url = reverse('mailing_add')
    response = api_client.post(url, data_mailing_2)

    assert response.status_code == 201
    assert Mailing.objects.count() == 2
    assert Mailing.objects.last().message == 'message two'
    assert Mailing.objects.last().filter_client == "tele2, filter two"


@pytest.mark.django_db
def test_mailing_api_mailing_update(api_client, mailing_1, data_mailing_2):
    """
    Тестирование обновления данных клиента по API.
    (PUT запрос)
    """
    assert Mailing.objects.count() == 0

    mailing_1.save()

    assert Mailing.objects.count() == 1
    assert Mailing.objects.first().message == 'message one'
    assert Mailing.objects.first().filter_client == "mts, filter one"

    url = reverse('mailing_up', kwargs={'pk': 1})
    response = api_client.put(url, data_mailing_2)

    assert response.status_code == 200
    assert Mailing.objects.count() == 1
    assert Mailing.objects.first().message == 'message two'
    assert Mailing.objects.first().filter_client == "tele2, filter two"


@pytest.mark.django_db
def test_mailing_api_mailing_delete(api_client, mailing_1, mailing_2):
    """
    Тестирование удаление клиента из БД по API.
    (DELETE запрос)
    """
    assert Mailing.objects.count() == 0

    mailing_1.save()
    mailing_2.save()

    assert Mailing.objects.count() == 2
    assert Mailing.objects.first().message == 'message one'
    assert Mailing.objects.last().filter_client == "tele2, filter two"

    url = reverse('mailing_del', kwargs={'pk': 2})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Mailing.objects.count() == 1
    assert Mailing.objects.last().message == 'message one'
    assert Mailing.objects.last().filter_client == "mts, filter one"

    url = reverse('mailing_del', kwargs={'pk': 1})
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Mailing.objects.count() == 0
