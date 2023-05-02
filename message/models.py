from django.db import models
from django.utils import timezone

class message(models.Model):
    sender=models.CharField(max_length=100,null=True)
    message_data=models.CharField(max_length=100,null=True)
    to=models.CharField(max_length=100,null=True)
    created=models.TimeField(default=timezone.now)
    def __str__(self):
        return str(self.message_data)
def get_name(ids):
    m=message.objects.get(id=ids)
    return m.message_data
class unreadmessage(models.Model):
    mess_id=models.IntegerField()
    def __str__(self):
        return get_name(self.mess_id)