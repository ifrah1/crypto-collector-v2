from django.contrib import admin

# import your models here
from .models import Crypto, Purchase, Feelings

# Register your models here
admin.site.register(Crypto)
admin.site.register(Purchase)
admin.site.register(Feelings)
