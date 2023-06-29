import datetime
import pytz

from mailing.models import Client


def get_clients(filter_client: str) -> list[Client]:
    """
    Возвращает список клиентов удовлетворяющих фильтру.

    :param filter_client: Фильтр клиентов. Состоит из кода оператора и тега.
                          прим.: "mts,tag1".

    :return: Список клиентов удовлетворяющих фильтру.
    """
    filter_lst = filter_client.split(',')
    right_clients = Client.objects.filter(code_phone=filter_lst[0].strip(),
                                          tag=filter_lst[1].strip()).all()
    return right_clients


def check_client_allowed_send_message(id_client: int) -> bool:
    """
    Проверяет можно ли по временному промежутку отправлять сообщение или нет.

    :param id_client: id клиента.
    :return: True если можно отправить сообщение, иначе False
    """
    try:
        client = Client.objects.get(pk=id_client)
        if not client:
            raise Exception('Клиента не существует')
        tz_client = pytz.timezone(client.timezone)

    except pytz.exceptions.UnknownTimeZoneError:
        raise Exception('У клиента указан неверный часовой пояс.')

    date_now = datetime.datetime.utcnow()
    time_client_now = tz_client.fromutc(date_now).time()

    start, end = formate_allow_time(allow_time=client.allow_time)

    return start < time_client_now < end


def formate_allow_time(allow_time: str) -> [datetime.time, datetime.time]:
    """
    Преобразует разрешенный временной промежуток (в виде строки "10:30-21:20")
    в объекты datetime.

    :param allow_time: временной промежуток (в виде строки "h:m-h:m")
    :return: datetime.time (только время) начала интервала и конца интервала.
    """
    if not allow_time:
        allow_time = '00:00-23:59'

    now = datetime.datetime.now()
    times_lst = allow_time.split('-')

    start = now.replace(hour=int(times_lst[0][:2]),
                        minute=int(times_lst[0][3:]),
                        second=0, microsecond=0)

    end = now.replace(hour=int(times_lst[1][:2]),
                      minute=int(times_lst[1][3:]),
                      second=0, microsecond=0)

    return start.time(), end.time()
