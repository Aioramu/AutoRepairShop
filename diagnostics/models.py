from django.db import models
from authorization.models import User
# Create your models here.

class Record(models.Model):
    time=models.DateTimeField(auto_now=False)
    SPECIALISTLIST=[
    ('motor', 'Мастер по моторам'),
    ('universal', 'Мастер по общим работам'),
    ('suspension', 'Мастер по обслуживанию подвески'),
    ('transmission', 'Мастер по кпп'),
    ]
    specialist=models.CharField(max_length=255,choices=SPECIALISTLIST)
    client=models.ForeignKey(User,on_delete=models.CASCADE)
