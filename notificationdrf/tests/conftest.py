import pytest

from mailing.models import Client, Mailing


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


# ------------------- Client start ---------------------------------------------
client_data_1 = {"phone": 79876543210,
                 "code_phone": 'mts',
                 "tag": "one",
                 "timezone": "Europe/Moscow",
                 "allow_time": "10:30-21:20"}

client_data_2 = {"phone": 77776543219,
                 "code_phone": 'tele2',
                 "tag": "two",
                 "timezone": "Europe/Vatican",
                 "allow_time": "18:15-19:45"}

client_data_3 = {"phone": 78776543219,
                 "code_phone": 'tele2',
                 "tag": "filter two",
                 "timezone": "Europe/Vatican",
                 "allow_time": "18:15-19:45"}


@pytest.fixture
def client_1():
    client = Client(phone=client_data_1["phone"],
                    code_phone=client_data_1["code_phone"],
                    tag=client_data_1["tag"],
                    timezone=client_data_1["timezone"])
    return client


@pytest.fixture
def client_2():
    client = Client(phone=client_data_2["phone"],
                    code_phone=client_data_2["code_phone"],
                    tag=client_data_2["tag"],
                    timezone=client_data_2["timezone"])
    return client


@pytest.fixture
def client_3():
    client = Client(phone=client_data_3["phone"],
                    code_phone=client_data_3["code_phone"],
                    tag=client_data_3["tag"],
                    timezone=client_data_3["timezone"])
    return client


@pytest.fixture
def data_client_1():
    return client_data_1


@pytest.fixture
def data_client_2():
    return client_data_2


@pytest.fixture
def data_client_3():
    return client_data_3


# ------------------- Client end -----------------------------------------------
# ------------------- Mailing start --------------------------------------------

mailing_data_1 = {"date_send": '2022-11-14 12:30',
                  "message": "message one",
                  "filter_client": "mts, filter one",
                  "date_send_end": '2022-11-24 16:45'}

mailing_data_2 = {"date_send": '2023-2-8 9:15',
                  "message": "message two",
                  "filter_client": "tele2, filter two",
                  "date_send_end": '2023-3-19 23:20'}


@pytest.fixture
def mailing_1():
    mailing = Mailing(date_send=mailing_data_1["date_send"],
                      message=mailing_data_1["message"],
                      filter_client=mailing_data_1["filter_client"],
                      date_send_end=mailing_data_1["date_send_end"])
    return mailing


@pytest.fixture
def mailing_2():
    mailing = Mailing(date_send=mailing_data_2["date_send"],
                      message=mailing_data_2["message"],
                      filter_client=mailing_data_2["filter_client"],
                      date_send_end=mailing_data_2["date_send_end"])
    return mailing


@pytest.fixture
def data_mailing_1():
    return mailing_data_1


@pytest.fixture
def data_mailing_2():
    return mailing_data_2


# ------------------- Mailing end ----------------------------------------------
# ------------------- Message start --------------------------------------------
# ------------------- Message end ----------------------------------------------
