from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cloth.models import Cloth_in_stock, Cloth_type, Color
from account.models import Revenue, Engaging, Sell_list, Selling, Engage_list

# Create your views here.

@login_required
def index(request):
    context = {}
    return render(request, 'ceo/index.html', context=context)

def graph(request):
    context = {}

    return render(request, 'ceo/graph.html', context=context)

def clothList():
    

    return None
