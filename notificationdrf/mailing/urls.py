from django.urls import path
from .views import ClientCreateAPIView, ClientUpAPIView, ClientDellAPIView, \
    MailingCreateAPIView, MailingUpAPIView, MailingDellAPIView, \
    MailingStatisticAllAPIView, MailingStatisticOneAPIView


urlpatterns = [
    # Client
    path('client/', ClientCreateAPIView.as_view(),
         name='client_add'),

    path('client/<int:pk>/', ClientUpAPIView.as_view(),
         name='client_up'),

    path('client_del/<int:pk>/', ClientDellAPIView.as_view(),
         name='client_del'),

    # Mailing
    path('mailing/', MailingCreateAPIView.as_view(),
         name='mailing_add'),

    path('mailing/<int:pk>/', MailingUpAPIView.as_view(),
         name='mailing_up'),

    path('mailing_del/<int:pk>/', MailingDellAPIView.as_view(),
         name='mailing_del'),

    # Mailing statistic
    path('mailing/statistic/', MailingStatisticAllAPIView.as_view(),
         name='statistics'),
    path('mailing/statistic/<int:pk>/', MailingStatisticOneAPIView.as_view(),
         name='statistic_one'),

]
