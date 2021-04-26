from django.db import models

# Import the reverse function
from django.urls import reverse

# Create your models here.

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

    # redirect once a new crypto is created
    def get_absolute_url(self):
        return reverse('detail', kwargs={'crypto_id': self.id})

# purchase model
class Purchase(models.Model):
    date = models.DateField('Purchase Date')
    purchase_price = models.IntegerField()
    total_amount = models.IntegerField()

    # Create a crypto_id FK 1:M
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bought {self.total_amount} on {self.date}"

    # change order of purchase 
    class Meta:
        ordering = ['-date']