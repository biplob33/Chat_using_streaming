from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from random import choice
from string import ascii_lowercase
def getency():
        return ''.join(choice(ascii_lowercase) for i in range(99))
class userdata(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    encpy=models.CharField(max_length=100,default=getency,unique=True)
    mob=models.IntegerField()
    online=models.BooleanField(default=False)
    last_active=models.DateTimeField(default=now)
    def __str__(self):
        return str(self.username)
