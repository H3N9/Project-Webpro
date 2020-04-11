from django.shortcuts import render, redirect
from .forms import Cloth_in_stockForm, Cloth_typeForm, ColorForm
from .models import Cloth_in_stock, Cloth_type, Color

# Create your views here.

def stock(request):
    context = {}
    stocks = Cloth_in_stock.objects.all()

    context['stocks'] = stocks
    return render(request, 'cloth/stock.html', context=context)

def color(request):
    context = {}
    form = ColorForm()
    if request.method=='POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Color.objects.create(name=data['name'],image=data['image'])
            return redirect('stock')
    context['form'] = form
    return render(request, 'cloth/color.html', context=context)

def cloth(request):
    context = {}
    form = Cloth_typeForm()
    if request.method=='POST':
        form = Cloth_typeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Cloth_type.objects.create(name=data['name'], cloth_desc=data['cloth_desc'])
            return redirect('stock')
    context['form'] = form
    return render(request, 'cloth/cloth.html', context=context)

def addStock(request):
    context = {}
    form = Cloth_in_stockForm()
    if request.method=='POST':
        form = Cloth_in_stockForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Cloth_in_stock.objects.create(
                quantity=data['quantity'],
                cloth_type=data['cloth_type'],
                color=data['color'],
                price=data['price'],
            )
            return redirect('stock')
    context['form'] = form
    return render(request, 'cloth/addStock.html', context=context)
