from mailing.models import Message, Mailing
from mailing.serializers import StatisticAllMailingsSerializer, \
    StatisticOneMailingSerializer


def get_statistic_all_mailings() -> list[dict]:
    """
    Возвращает список с общими данными по каждый рассылке.
    """
    try:
        all_total_messages = Message.objects.count()
        all_successful = Message.objects.filter(status=1).count()
        all_failed = all_total_messages - all_successful

        title = {'Всего сообщений отправлено': all_total_messages,
                 'Успешных отправок сообщений': all_successful,
                 'Неудачных отправок сообщений': all_failed}

        mailings = Mailing.objects.all()
    except Exception as e:
        raise {'ERROR': f'Ошибка с БД {e}'}

    datas = list()
    datas.append(title)

    for mailing in mailings:
        total_messages = Message.objects.filter(mailing=mailing.pk).count()
        successful = Message.objects.filter(mailing=mailing.pk,
                                            status=1).count()
        failed = total_messages - successful

        item = {'mailing_id': mailing.pk,
                'message': mailing.message,
                'total': total_messages,
                'successful': successful,
                'failed': failed}

        serializer = StatisticAllMailingsSerializer(data=item)
        if serializer.is_valid():
            datas.append(serializer.data)

    return datas


def get_statistic_one_mailing(mailing_id: int) -> list[dict]:
    """
    Возвращает список с подробными данными по каждому сообщению рассылки.
    """
    mailing = Mailing.objects.filter(pk=mailing_id).first()
    if not mailing:
        return []
    messages = Message.objects.filter(mailing=mailing.pk)

    all_total_messages = messages.count()
    all_successful = Message.objects.filter(mailing=mailing.pk,
                                            status=1).count()
    all_failed = all_total_messages - all_successful

    datas = list()

    title = {'ID рассылки': mailing.pk,
             'Текст': mailing.message,
             'Фильтр': mailing.filter_client,
             'Дата начала': mailing.date_send,
             'Дата завершения': mailing.date_send_end,
             'Общее кол-во сообщений': all_total_messages,
             'Успешных отправок сообщений': all_successful,
             'Неудачных отправок сообщений': all_failed}
    datas.append(title)

    for message in messages:
        item = {'date': message.date_create,
                'phone': message.client.phone,
                'status': message.status}

        serializer = StatisticOneMailingSerializer(data=item)
        if serializer.is_valid():
            datas.append(serializer.data)

    return datas
