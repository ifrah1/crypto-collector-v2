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
    # add purchases for a crypto
    path('cryptos/<int:crypto_id>/add_purchase/', views.add_purchase, name='add_purchase'), 

    # associate a feeling with a crypto (M:M)
    path('cryptos/<int:crypto_id>/assoc_feeling/<int:feeling_id>/', views.assoc_feeling, name='assoc_feeling'), 

    # remove a feelings with a crypto (M:M)
    path('cryptos/<int:crypto_id>/remove_feeling/<int:feeling_id>/', views.remove_feeling, name='remove_feeling'),

    # add a photo for a crypto
    path('cryptos/<int:crypto_id>/add_photo/', views.add_photo, name='add_photo'),

    # feelings urls
    path('feelings/', views.feelings_index, name='feelings_all'),
    path('feelings/<int:feeling_id>/', views.feeling_detail, name='feeling_detail'),
    path('feelings/create/', views.FeelingsCreate.as_view(), name='feelings_create'),
    path('feelings/<int:pk>/update/', views.FeelingsUpdate.as_view(), name='feelings_update'),
    path('feelings/<int:pk>/delete/', views.FeelingsDelete.as_view(), name='feelings_delete'),

    # user account paths:
    path('accounts/signup/', views.signup, name='signup'),
]