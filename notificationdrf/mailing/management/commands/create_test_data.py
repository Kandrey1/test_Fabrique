"""
Команда добавляет тестовые данные для отладки.
"""
import random

from django.core.management.base import BaseCommand
from mailing.models import Client, Mailing, Message


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:

        timezones = ['Europe/Samara', 'Europe/Moscow', 'Europe/Simferopol',
                     'Europe/Astrakhan']
        tags = ['t_one', 't_two', 't_three']

        codes_phone = ['mts', 'megafon', 'tele2', 'yota']

        phone_base = 7654321

        # Создание клиентов
        for i in range(100):
            code = random.choice(['123', '234', '345', '543', '568', '921'])
            phone = f'7{code}{phone_base + i}'

            client = Client(phone=phone,
                            code_phone=random.choice(codes_phone),
                            tag=random.choice(tags),
                            timezone=random.choice(timezones))
            client.save()

        # Создание рассылок
        for i in range(5):
            d_start = str(random.randint(1, 30))
            d_end = str(random.randint(1, 30))
            mailing = Mailing(date_send=f'2023-5-{d_start} 20:20',
                              message=f"message {i}",
                              filter_client=f'{random.choice(codes_phone)},'
                                            f'{random.choice(tags)}',
                              date_send_end=f'2023-6-{d_end} 10:20')
            mailing.save()

        mailings = Mailing.objects.all()
        clients = Client.objects.all()

        # Создание сообщений
        for i in range(100):
            message = Message(status=random.choice([True, False]),
                              mailing=random.choice(mailings),
                              client=random.choice(clients),
                              )
            message.save()
