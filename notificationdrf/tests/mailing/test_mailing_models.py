import datetime
import pytest
import pytz

from mailing.models import Client, Mailing, Message


@pytest.mark.django_db
def test_table_client(client_1, client_2):
    """
    Тестирование модели Client
    """
    client_1.save()

    assert Client.objects.count() == 1
    assert Client.objects.first().phone == 79876543210
    assert Client.objects.first().code_phone == 'mts'
    assert Client.objects.first().tag == "one"
    assert Client.objects.first().timezone == 'Europe/Moscow'

    client_2.save()

    assert Client.objects.count() == 2
    assert Client.objects.last().phone == 77776543219
    assert Client.objects.last().code_phone == 'tele2'
    assert Client.objects.last().tag == "two"
    assert Client.objects.last().timezone == 'Europe/Vatican'


@pytest.mark.django_db
def test_table_mailing(mailing_1, mailing_2):
    """
    Тестирование модели Mailing
    """
    mailing_1.save()

    dt1_1 = datetime.datetime(2022, 11, 14, hour=12, minute=30,
                              tzinfo=pytz.timezone('UTC'))
    dt1_2 = datetime.datetime(2022, 11, 24, hour=16, minute=45,
                              tzinfo=pytz.timezone('UTC'))

    assert Mailing.objects.count() == 1
    assert Mailing.objects.first().date_send == dt1_1
    assert Mailing.objects.first().message == "message one"
    assert Mailing.objects.first().filter_client == "mts, filter one"
    assert Mailing.objects.first().date_send_end == dt1_2

    mailing_2.save()

    dt2_1 = datetime.datetime(2023, 2, 8, hour=9, minute=15,
                              tzinfo=pytz.timezone('UTC'))
    dt2_2 = datetime.datetime(2023, 3, 19, hour=23, minute=20,
                              tzinfo=pytz.timezone('UTC'))

    assert Mailing.objects.count() == 2
    assert Mailing.objects.last().date_send == dt2_1
    assert Mailing.objects.last().message == "message two"
    assert Mailing.objects.last().filter_client == "tele2, filter two"
    assert Mailing.objects.last().date_send_end == dt2_2


@pytest.mark.django_db
def test_table_message(client_1, client_2, mailing_1):
    """
    Тестирование модели Message
    """
    client_1.save()
    client_2.save()

    assert Client.objects.count() == 2

    mailing_1.save()

    assert Mailing.objects.count() == 1

    message = Message(date_create='2022-11-14 12:30',
                      status=True,
                      mailing=mailing_1,
                      client=client_2)

    message.save()

    assert Message.objects.count() == 1
    assert Message.objects.first().status is True
    assert Message.objects.first().mailing.pk == 1
    assert Message.objects.first().client.pk == 2
