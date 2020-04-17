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
    colors = Color.objects.all()
    context['colors'] = colors
    return render(request, 'cloth/color.html', context=context)

def cloth(request):
    context = {}
    cloths = Cloth_type.objects.all()
    context['cloths'] = cloths
    return render(request, 'cloth/cloth.html', context=context)

def clothAdd(request):
    context = {}
    form = Cloth_typeForm()
    if request.method=='POST':
        form = Cloth_typeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Cloth_type.objects.create(name=data['name'], cloth_desc=data['cloth_desc'])
            return redirect('stock')
    context['form'] = form
    return render(request, 'cloth/clothAdd.html', context=context)

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

def clothEdit(request, cid):
    cloth = Cloth_type.objects.get(pk=cid)
    form = Cloth_typeForm(instance=cloth)
    if request.method == "POST":
        form = Cloth_typeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cloth.name = data['name']
            cloth.cloth_desc = data['cloth_desc']
            cloth.save()
            return redirect('cloth')
    return render(request, 'cloth/clothEdit.html', context={'cloth':cloth,'form':form})


def colorEdit(request, cid):
    color = Color.objects.get(pk=cid)
    form = ColorForm(instance=color)
    if request.method == "POST":
        form = ColorForm(request.POST, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            color.name = data['name']
            color.image = data['image']
            color.save()
            return redirect('color')
    return render(request, 'cloth/colorEdit.html', context={'color':color,'form':form})

def colorAdd(request):
    context = {}
    form = ColorForm()
    if request.method=='POST':
        form = ColorForm(request.POST, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            add = Color.objects.create(name=data['name'],image=data['image'])
            return redirect('color')
    context['form'] = form
    return render(request, 'cloth/colorAdd.html', context=context)
