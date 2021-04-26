from django.contrib import admin

# import your models here
from .models import Crypto

# Register your models here
admin.site.register(Crypto)
