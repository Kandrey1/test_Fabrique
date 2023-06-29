from django.http import JsonResponse
from rest_framework import generics

from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer, \
    StatisticAllMailingsSerializer, StatisticOneMailingSerializer
from .services import get_statistic_all_mailings, get_statistic_one_mailing


class ClientCreateAPIView(generics.CreateAPIView):
    """
    Добавления нового клиента. В запросе должен быть JSON формата:

    "timezone" должно быть в формате "Europe/Moscow"
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientUpAPIView(generics.UpdateAPIView):
    """
    Обновление данных клиента, в запросе должен быть JSON формата:

    "timezone" должно быть в формате "Europe/Moscow"
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDellAPIView(generics.DestroyAPIView):
    """
    Удаляет клиента из БД, по его id.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingCreateAPIView(generics.CreateAPIView):
    """
    Добавление рассылки. В запросе должен быть JSON формата:

    Дата должна быть в формате 'Year-month-day hour:minute'
    прим.:'2022-11-14 12:30'
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingUpAPIView(generics.UpdateAPIView):
    """
    Обновление данных рассылки, в запросе должен быть JSON формата:

    Дата должна быть в формате 'Year-month-day hour:minute'
    прим.:'2022-11-14 12:30'
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDellAPIView(generics.DestroyAPIView):
    """
    Удаляет рассылку из БД, по её id.
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatisticAllAPIView(generics.GenericAPIView):
    """
    Получение краткой статистики по всем рассылкам в БД.
    """
    serializer_class = StatisticAllMailingsSerializer
    queryset = ''

    def get(self, request, *args, **kwargs):
        return JsonResponse(get_statistic_all_mailings(), safe=False)


class MailingStatisticOneAPIView(generics.GenericAPIView):
    """
    Получение подробной статистики рассылке.
    """
    serializer_class = StatisticOneMailingSerializer
    queryset = ''

    def get(self, request, *args, **kwargs):
        mailing_id = self.kwargs.get('pk')
        return JsonResponse(get_statistic_one_mailing(mailing_id), safe=False)
