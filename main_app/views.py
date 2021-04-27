from django.shortcuts import render, redirect

# import models
from .models import Crypto, Feelings, Photo

# class based views
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# import purchase form
from .forms import PurchaseForm

# aws sdk for uploading to s3
import boto3
import uuid

# variables needed for s4 buckets
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'crypto-collector'

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
    
    # This inherited method is called when a
    # valid crypto form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the crypto
        # Let the CreateView do its job as usual
        return super().form_valid(form)

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

# add a feeling to a crypto
def assoc_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.add(feeling_id)
    return redirect('detail', crypto_id=crypto_id)


def remove_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.remove(feeling_id)
    return redirect('detail', crypto_id=crypto_id)


# adds a photo 
def add_photo(request, crypto_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to crypto_id or crypto (if you have a crypto object)
            photo = Photo(url=url, crypto_id=crypto_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', crypto_id=crypto_id)