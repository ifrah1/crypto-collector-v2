from django.shortcuts import render

from django.shortcuts import render


class Crypto:  # Note that parens are optional if not inheriting from another class
    def __init__(self, name, price, description, amount):
        self.name = name
        self.price = price
        self.description = description
        self.amount = amount

cryptos = [
    Crypto('litecoin', 300, 'fast coin', 3),
    Crypto('bitcoin', 50000, 'OG', 0),
]
# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# Add new view
def cryptos_index(request):
    return render(request, 'cryptos/index.html', { 'cryptos': cryptos })