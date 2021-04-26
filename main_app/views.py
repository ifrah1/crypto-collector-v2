from django.shortcuts import render

# import models
from .models import Crypto

# class based views
from django.views.generic.edit import CreateView

# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# Add new view
def cryptos_index(request):
    cryptos = Crypto.objects.all()
    return render(request, 'cryptos/index.html', { 'cryptos': cryptos })

# individual crypto detail page
def cryptos_detail(request, crypto_id):
    crypto = Crypto.objects.get(id=crypto_id)
    return render(request, 'cryptos/detail.html',{'crypto': crypto})

# create a new crypto view
class CryptoCreate(CreateView):
    model = Crypto
    #fields = '__all__'  # does all form
    fields = ['name', 'price', 'description', 'amount'] # what fields we want in form
    #success_url = '/cryptos/'