import datetime

import requests
from celery import shared_task

from mailing.models import Message, Mailing, Client
from mailing.sevice_selery import get_clients, check_client_allowed_send_message
from notificationdrf import settings


@shared_task
def period_task_start_mailing():
    """
    Периодическая задача. Вызывается автоматически через определенный
    промежуток времени. Запускает новые рассылки.
    """
    try:
        start_new_mailing.delay()
    except Exception as e:
        print(f'Error, period_task_start_mailing <{e}>')


@shared_task
def start_new_mailing():
    """
    Запускает новые рассылки.

    Ищет рассылки, которые действуют на данные момент времени.
    Создает список клиентов подходящих под фильтр данной рассылки.
    Проверяет можно ли отправить клиенту сообщение. Если можно отправляет.

    """
    try:
        date_now = datetime.datetime.now()
        mailings = Mailing.objects.filter(date_send__lt=date_now,
                                          date_send_end__gt=date_now).all()

        for mailing in mailings:
            clients = get_clients(mailing.filter_client)

            for client in clients:
                # Проверка, можно ли отправить сообщение клиенту сейчас.
                if check_client_allowed_send_message(client.pk):

                    # Проверка, было сообщение отправлено ранее или нет.
                    msg = Message.objects.filter(mailing=mailing.pk,
                                                 client=client.pk).first()

                    # Если сообщение было доставлено,то переход к след. клиенту.
                    if msg.status:
                        continue

                    # Если сообщение не отправлялось, создает.
                    if not msg:
                        msg = Message(status=False,
                                      mailing=mailing,
                                      client=Client.objects.get(pk=client.pk))
                        msg.save()

                    # Отправка сообщения клиенту
                    send_message_client.delay(msg_id=msg.pk,
                                              phone=client.phone,
                                              text=mailing.message)
    except Exception as e:
        print(f'Error, start_new_mailing <{e}>')


@shared_task
def send_message_client(msg_id: int, phone: int, text: str):
    """
    Отправляет сообщение клиенту.
    Отправляет сообщение на вспомогательный сервис в
    Тестовом задании "https://probe.fbrq.cloud/"

    :param msg_id: ID сообщения в БД.
    :param phone: Номер телефона клиента, на который нужно отправить сообщение.
    :param text: Текст сообщения.

    :return True если сообщение доставлено, иначе False.
    """
    headers = {'Authorization': f'Bearer {settings.TOKEN_ACCESS}'}
    data = {
        "id": msg_id,
        "phone": phone,
        "text": text
    }
    url = f'https://probe.fbrq.cloud/v1/send/{msg_id}'

    try:
        res = requests.post(url=url, json=data, headers=headers)

        msg = Message.objects.get(pk=msg_id)
        msg.status = True if res.status_code == 200 else False
        msg.save()
    except Exception as e:
        print(f'Error, send_message_client <{e}>')
