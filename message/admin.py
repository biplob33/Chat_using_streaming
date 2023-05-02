from django.contrib import admin
from message.models import message,unreadmessage
admin.site.register(message)
admin.site.register(unreadmessage)