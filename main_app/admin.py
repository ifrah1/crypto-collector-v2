from django.contrib import admin

# import your models here
from .models import Crypto, Purchase

# Register your models here
admin.site.register(Crypto)
admin.site.register(Purchase)
