from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Рассылка уведомлений",
        default_version='v1',
        description="API для сервиса рассылки уведомлений",
    ),
    patterns=[path('api/v1/', include('mailing.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/v1/', include('mailing.urls')),
    path('docs/',
         TemplateView.as_view(
             template_name='swaggerui/swaggerui.html',
             extra_context={'schema_url': 'openapi-schema'}),
         name='swagger'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
]
