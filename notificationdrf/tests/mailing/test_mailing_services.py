import pytest

from mailing.models import Client, Mailing, Message
from mailing.services import get_statistic_one_mailing, \
    get_statistic_all_mailings


@pytest.mark.django_db
def test_statistic_all_mailings(client_1, client_2, mailing_1, mailing_2):
    """
    Тестирование сервиса получения краткой статистики по всем рассылкам.
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

    datas = get_statistic_all_mailings()

    good_datas = [{'Всего сообщений отправлено': 3,
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

    assert datas
    assert datas == good_datas


@pytest.mark.django_db
def test_statistic_one_mailing(client_1, client_2, mailing_1, mailing_2):
    """
    Тестирование сервиса получения полной статистики по одной рассылке.
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

    datas = get_statistic_one_mailing(mailing_id=1)

    good_datas = [{'ID рассылки': 1,
                  'Текст': 'message one',
                   'Фильтр': 'mts, filter one',
                   'Дата начала': '2022-11-14T12:30:00Z',
                   'Дата завершения': '2022-11-24T16:45:00Z',
                   'Общее кол-во сообщений': 2,
                   'Успешных отправок сообщений': 1,
                   'Неудачных отправок сообщений': 1}]
    assert datas
    assert datas[0]['Фильтр'] == good_datas[0]['Фильтр']
    assert datas[0]['Общее кол-во сообщений'] == good_datas[0]['Общее кол-во сообщений']
