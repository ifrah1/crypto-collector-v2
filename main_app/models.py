from django.db import models

# Create your models here.

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    amount = models.IntegerField()
