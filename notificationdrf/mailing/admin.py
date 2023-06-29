from django.contrib import admin
from . import models


class ClientAdmin(admin.ModelAdmin):
    pass


class MailingAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Mailing, MailingAdmin)
admin.site.register(models.Message, MessageAdmin)
