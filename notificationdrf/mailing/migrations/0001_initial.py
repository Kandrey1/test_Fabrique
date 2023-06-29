# Generated by Django 4.2.1 on 2023-05-20 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(help_text='Номер телефона', unique=True)),
                ('code_phone', models.CharField(help_text='Код оператора', max_length=100)),
                ('tag', models.CharField(help_text='Тег', max_length=150)),
                ('timezone', models.CharField(help_text='Часовой пояс', max_length=100)),
                ('allow_time', models.CharField(help_text='Разрешенный промежуток времени', max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_send', models.DateTimeField(help_text='Дата начала рассылки')),
                ('message', models.CharField(help_text='Сообщение рассылки', max_length=300)),
                ('filter_client', models.CharField(help_text='Фильтр', max_length=200)),
                ('date_send_end', models.DateTimeField(help_text='Дата окончания рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now=True, help_text='Дата создания сообщения')),
                ('status', models.BooleanField(help_text='Успешна или нет отправка')),
                ('client', models.ForeignKey(help_text='Клиент которому было отправлено сообщение.', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.client')),
                ('mailing', models.ForeignKey(help_text='Рассылка, в рамках которой было отправлено сообщение', on_delete=django.db.models.deletion.PROTECT, related_name='messages', to='mailing.mailing')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['id'],
            },
        ),
    ]