import datetime

import pytest

from mailing.models import Client
from mailing.sevice_selery import get_clients, formate_allow_time


@pytest.mark.django_db
def test_get_clients(client_1, client_2, client_3, mailing_2):
    """
    Тестирование получения списка клиентов прошедших фильтр.
    """
    assert Client.objects.count() == 0
    client_1.save()
    client_2.save()
    client_3.save()

    assert Client.objects.count() == 3

    mailing_2.save()

    lst_clients = get_clients(mailing_2.filter_client)

    assert len(lst_clients) == 1
    assert lst_clients[0].phone == 78776543219
    assert lst_clients[0].code_phone == 'tele2'


@pytest.mark.django_db
def test_formate_allow_time():
    """
    Тестирование функции преобразующей разрешенный временной
    промежуток (в виде строки "10:30-21:20") в объекты datetime.
    """
    allow_string = "10:30-21:20"
    start_answer = datetime.datetime(year=1900, month=1, day=1,
                                     hour=10, minute=30,
                                     second=0, microsecond=0)

    end_answer = datetime.datetime(year=1900, month=1, day=1,
                                   hour=21, minute=20,
                                   second=0, microsecond=0)

    start, end = formate_allow_time(allow_string)

    assert start_answer.time() == start
    assert end_answer.time() == end
