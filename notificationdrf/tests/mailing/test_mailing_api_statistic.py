import pytest
from django.urls import reverse

from mailing.models import Mailing, Client, Message


@pytest.mark.django_db
def test_mailing_api_statistic_all(api_client, client_1, client_2, mailing_1,
                                   mailing_2):
    """
    Тестирование получения краткой статистики по всем рассылкам.
    """
    assert Client.objects.count() == 0
    client_1.save()
    client_2.save()

    assert Client.objects.count() == 2

    assert Mailing.objects.count() == 0
    mailing_1.save()
    mailing_2.save()

    assert Mailing.objects.count() == 2

    message_1 = Message(status=True, mailing=mailing_1, client=client_1)
    message_1.save()
    message_2 = Message(status=False, mailing=mailing_1, client=client_2)
    message_2.save()
    message_3 = Message(status=True, mailing=mailing_2, client=client_1)
    message_3.save()

    # проверка доступа без токена
    url = reverse('statistics')
    response = api_client.get(url)

    good_response = [{'Всего сообщений отправлено': 3,
                      'Успешных отправок сообщений': 2,
                      'Неудачных отправок сообщений': 1},
                     {'mailing_id': 1, 'message':
                      'message one', 'total': 2,
                      'successful': 1,
                      'failed': 1},
                     {'mailing_id': 2,
                      'message': 'message two',
                      'total': 1,
                      'successful': 1,
                      'failed': 0}]

    assert response.status_code == 200
    assert response.json() == good_response


@pytest.mark.django_db
def test_mailing_api_statistic_one(api_client, client_1, client_2, mailing_1,
                                   mailing_2):
    """
    Тестирование получения полной статистики по одной рассылке.
    """
    assert Client.objects.count() == 0
    client_1.save()
    client_2.save()

    assert Client.objects.count() == 2

    assert Mailing.objects.count() == 0
    mailing_1.save()
    mailing_2.save()

    assert Mailing.objects.count() == 2

    message_1 = Message(status=True, mailing=mailing_1, client=client_1)
    message_1.save()
    message_2 = Message(status=False, mailing=mailing_1, client=client_2)
    message_2.save()
    message_3 = Message(status=True, mailing=mailing_2, client=client_1)
    message_3.save()

    url = reverse('statistic_one', kwargs={'pk': 1})
    response = api_client.get(url)

    good_response = [{'ID рассылки': 1,
                      'Текст': 'message one',
                      'Фильтр': 'mts, filter one',
                      'Дата начала': '2022-11-14T12:30:00Z',
                      'Дата завершения': '2022-11-24T16:45:00Z',
                      'Общее кол-во сообщений': 2,
                      'Успешных отправок сообщений': 1,
                      'Неудачных отправок сообщений': 1},
                     {'date': f'{message_1.date_create}',
                      'phone': 79876543210,
                      'status': True},
                     {'date': f'{message_2.date_create}',
                      'phone': 77776543219,
                      'status': False}]

    assert response.status_code == 200
    assert response.json()[0] == good_response[0]
    assert response.json()[1]['phone'] == good_response[1]['phone']
    assert response.json()[2]['phone'] == good_response[2]['phone']
