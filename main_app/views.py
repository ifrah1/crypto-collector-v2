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

# imports for login and creation 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

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
@login_required
def cryptos_index(request):
    cryptos = Crypto.objects.filter(user=request.user)
    # You could also retrieve the logged in user's cats like this
    # cats = request.user.cat_set.all()
    return render(request, 'cryptos/index.html', { 'cryptos': cryptos })

# individual crypto detail page
@login_required
def cryptos_detail(request, crypto_id):
    crypto = Crypto.objects.get(id=crypto_id)
    
    # Get the feelings for crypto doesn't have
    feelings_crypto_doesnt_have = Feelings.objects.exclude(id__in = crypto.feelings.all().values_list('id'))

    # instantiate PurchaseForm to be rendered in the template
    purchase_form = PurchaseForm()

    return render(request, 'cryptos/detail.html',{'crypto': crypto, 'purchase_form': purchase_form, 'feelings': feelings_crypto_doesnt_have})

# adds purchase to crypto
@login_required
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
class CryptoCreate(LoginRequiredMixin,CreateView):
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
class CryptoUpdate(LoginRequiredMixin,UpdateView):
    model = Crypto
    # Let's disallow the renaming of a crypto by excluding the name field!
    fields = ['price', 'description', 'amount']

# delete a crypto view
class CryptoDelete(LoginRequiredMixin,DeleteView):
    model = Crypto
    success_url = '/cryptos/'


# feelings views -*-*-*-*-*-*-*-
# Add new view
@login_required
def feelings_index(request):
    feelings = Feelings.objects.all()
    return render(request, 'feeling/index.html', { 'feelings': feelings })

# individual crypto detail page
def feeling_detail(request, feeling_id):
    feeling = Feelings.objects.get(id=feeling_id)
    return render(request, 'feeling/detail.html',{'feeling': feeling})

# create a new crypto view
class FeelingsCreate(LoginRequiredMixin,CreateView):
    model = Feelings
    fields = ['status', 'color']

class FeelingsUpdate(LoginRequiredMixin,UpdateView):
    model = Feelings
    fields = ['status', 'color']

class FeelingsDelete(LoginRequiredMixin,DeleteView):
    model = Feelings
    success_url = '/feelings/'

# add a feeling to a crypto
@login_required
def assoc_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.add(feeling_id)
    return redirect('detail', crypto_id=crypto_id)

@login_required
def remove_feeling(request, crypto_id, feeling_id):
    # Note that you can pass a feeling's id instead of the whole object
    Crypto.objects.get(id=crypto_id).feelings.remove(feeling_id)
    return redirect('detail', crypto_id=crypto_id)


# adds a photo 
@login_required
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


# sign up functions to create users
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)