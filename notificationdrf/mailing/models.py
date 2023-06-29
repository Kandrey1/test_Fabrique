from django.db import models


class Client(models.Model):
    """
    Модель данных клиента.

    phone: Номер телефона клиента.
    code_phone: Код оператора связи клиента.
    tag: Тег клиента
    timezone: Часовой пояс.
    allow_time: Разрешенный промежуток времени для оправки сообщений.
        Промежуток времени должен быть в формате
        "Hour:minute-Hour:minute" прим.: "11:30-16:15"

    """
    phone = models.IntegerField(unique=True,
                                help_text='Номер телефона')
    code_phone = models.CharField(max_length=100,
                                  help_text='Код оператора')
    tag = models.CharField(max_length=150,
                           help_text='Тег')
    timezone = models.CharField(max_length=100,
                                help_text='Часовой пояс')
    allow_time = models.CharField(max_length=20,
                                  null=True,
                                  help_text='Разрешенный промежуток времени')

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = 'Клиенты'
        ordering = ["id"]

    def __str__(self):
        return str(self.phone)


class Mailing(models.Model):
    """
    Модель данных рассылки.

    date_send: дата начала рассылки.
    message: сообщение рассылки.
    filter_client: фильтр свойств клиентов, на которых должна быть произведена
                   рассылка (код мобильного оператора, тег).
    date_send_end: дата окончания рассылки.

    Даты должны быть в формате 'Year-month-day hour:minute'
    прим.:'2022-11-14 12:30'

    """
    date_send = models.DateTimeField(help_text='Дата начала рассылки')
    message = models.CharField(max_length=300,
                               help_text='Сообщение рассылки')
    filter_client = models.CharField(max_length=200,
                                     help_text='Фильтр')
    date_send_end = models.DateTimeField(help_text='Дата окончания рассылки')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = 'Рассылки'
        ordering = ["id"]

    def __str__(self):
        return f"{self.date_send} - {self.message}"


class Message(models.Model):
    """
    Модель данных состояния отправки сообщения.

    date_create: дата и время создания (отправки).
    status: статус отправки.
    mailing: id рассылки, в рамках которой было отправлено сообщение.
    client: id клиента, которому отправили.

    """
    date_create = models.DateTimeField(auto_now=True,
                                       blank=True,
                                       help_text='Дата создания сообщения')
    status = models.BooleanField(help_text='Успешна или нет отправка')
    mailing = models.ForeignKey('Mailing',
                                on_delete=models.PROTECT,
                                related_name='messages',
                                help_text='Рассылка, в рамках которой было'
                                          ' отправлено сообщение')
    client = models.ForeignKey('Client',
                               on_delete=models.CASCADE,
                               related_name='messages',
                               help_text='Клиент которому было отправлено'
                                         ' сообщение.')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'
        ordering = ["id"]

    def __str__(self):
        return f"{self.pk}:{self.mailing} - {self.date_create} -" \
               f" {self.status} - {self.client}"
