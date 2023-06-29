from rest_framework import serializers
from .models import Client, Message, Mailing


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Клиент.
    """
    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели сообщение.
    """
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели рассылка.
    """
    class Meta:
        model = Mailing
        fields = '__all__'


class StatisticAllMailingsSerializer(serializers.Serializer):
    """
    Сериалайзер для запроса общих данных рассылок.
    """
    mailing_id = serializers.IntegerField(help_text='id рассылки')
    message = serializers.CharField(max_length=250, help_text='Текст сообщения')
    total = serializers.IntegerField(help_text='Всего сообщений')
    successful = serializers.IntegerField(help_text='Успешных отправок')
    failed = serializers.IntegerField(help_text='Неудачных отправок')


class StatisticOneMailingSerializer(serializers.Serializer):
    """
    Сериалайзер для данных по одной рассылке.
    """
    date = serializers.DateTimeField(help_text='Дата отправки сообщения')
    phone = serializers.IntegerField(help_text='Телефон отправки')
    status = serializers.BooleanField(help_text='Статус отправки')
