from django.shortcuts import render, redirect

# import models
from .models import Crypto, Feelings

# class based views
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# import purchase form
from .forms import PurchaseForm

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
    
    # Get the feelings for crypto doesn't have
    feelings_crypto_doesnt_have = Feelings.objects.exclude(id__in = crypto.feelings.all().values_list('id'))

    # instantiate PurchaseForm to be rendered in the template
    purchase_form = PurchaseForm()

    return render(request, 'cryptos/detail.html',{'crypto': crypto, 'purchase_form': purchase_form, 'feelings': feelings_crypto_doesnt_have})

# adds purchase to crypto
def add_purchase(request, crypto_id):
    # create the ModelForm using the data in request.POST
    form = PurchaseForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the crypto_id assigned
        new_purchase = form.save(commit=False)
        new_purchase.crypto_id = crypto_id
        new_purchase.save()
    return redirect('detail', crypto_id=crypto_id)

# create a new crypto view
class CryptoCreate(CreateView):
    model = Crypto
    #fields = '__all__'  # does all form
    fields = ['name', 'price', 'description', 'amount'] # what fields we want in form
    #success_url = '/cryptos/'

# update a crypto view
class CryptoUpdate(UpdateView):
    model = Crypto
    # Let's disallow the renaming of a crypto by excluding the name field!
    fields = ['price', 'description', 'amount']

# delete a crypto view
class CryptoDelete(DeleteView):
    model = Crypto
    success_url = '/cryptos/'


# feelings views -*-*-*-*-*-*-*-
# Add new view
def feelings_index(request):
    feelings = Feelings.objects.all()
    return render(request, 'feeling/index.html', { 'feelings': feelings })

# individual crypto detail page
def feeling_detail(request, feeling_id):
    feeling = Feelings.objects.get(id=feeling_id)
    return render(request, 'feeling/detail.html',{'feeling': feeling})

# create a new crypto view
class FeelingsCreate(CreateView):
    model = Feelings
    fields = ['status', 'color']

class FeelingsUpdate(UpdateView):
    model = Feelings
    fields = ['status', 'color']

class FeelingsDelete(DeleteView):
    model = Feelings
    success_url = '/feelings/'