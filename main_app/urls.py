from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for cryptos index
    path('cryptos/', views.cryptos_index, name='index'),
    path('cryptos/<int:crypto_id>/', views.cryptos_detail, name='detail'), 

    # route used to show a form and create a crypto
    path('cryptos/create/', views.CryptoCreate.as_view(), name='cryptos_create'), 
    # update a crypto
    path('cryptos/<int:pk>/update/', views.CryptoUpdate.as_view(), name='cryptos_update'),
    # delete a crypto
    path('cryptos/<int:pk>/delete/', views.CryptoDelete.as_view(), name='cryptos_delete'),
]