from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for cryptos index
    path('cryptos/', views.cryptos_index, name='index'),
    path('cryptos/<int:crypto_id>/', views.cryptos_detail, name='detail'), 
]