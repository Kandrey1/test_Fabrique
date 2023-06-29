"""
Команда добавляет администратора.
Данные для регистрации берутся из файла .env
"""
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

name_admin = os.environ.get('SUPERUSER_USERNAME')
pass_admin = os.environ.get('SUPERUSER_PASSWORD')
email_admin = os.environ.get('SUPERUSER_EMAIL')


class Command(BaseCommand):

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.filter(username=name_admin).first()
        if not user:
            get_user_model().objects.create_superuser(username=name_admin,
                                                      password=pass_admin,
                                                      email=email_admin)
