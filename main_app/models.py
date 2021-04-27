from django.db import models

# Import the reverse function
from django.urls import reverse

# Import the User
from django.contrib.auth.models import User

# Create your models here.
# feelings model
class Feelings(models.Model):
    status = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    # Other goodness such as 'def __str__():' below
    def __str__(self):
        return f'{self.status} {self.color}'
    # fixed redirection issue once 
    def get_absolute_url(self):
        return reverse('feeling_detail', kwargs={'feeling_id': self.id}) 

# crypto model
class Crypto(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=250)
    amount = models.IntegerField()

    # Add the M:M relationship
    feelings = models.ManyToManyField(Feelings)

    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

# photo model
class Photo(models.Model):
    url = models.CharField(max_length=200)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for crypto_id: {self.crypto_id} @{self.url}"