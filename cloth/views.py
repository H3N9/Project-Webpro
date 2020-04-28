from django.shortcuts import render, redirect
from .forms import Cloth_in_stockForm, Cloth_typeForm, ColorForm
from .models import Cloth_in_stock, Cloth_type, Color
from project.check import group_required
# Create your views here.
@group_required('manager')
def stock(request):
    context = {}
    stocks = Cloth_in_stock.objects.all().order_by('-quantity')
    context['stocks'] = stocks
    return render(request, 'cloth/stock.html', context=context)

@group_required('manager')
def color(request):
    context = {}
    colors = Color.objects.all().order_by('name')
    context['colors'] = colors
    return render(request, 'cloth/color.html', context=context)

@group_required('manager')
def cloth(request):
    context = {}
    cloths = Cloth_type.objects.all().order_by('name')
    context['cloths'] = cloths
    return render(request, 'cloth/cloth.html', context=context)

@group_required('manager')
def clothAdd(request):
    context = {}
    form = Cloth_typeForm()
    if request.method=='POST':
        form = Cloth_typeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Cloth_type.objects.create(name=data['name'], cloth_desc=data['cloth_desc'])
            return redirect('cloth')
    context['form'] = form
    return render(request, 'cloth/clothAdd.html', context=context)

@group_required('manager')
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

@group_required('manager')
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


@group_required('manager')
def colorEdit(request, cid):
    color = Color.objects.get(pk=cid)
    form = ColorForm()
    if request.method == "POST":
        form = ColorForm(request.POST, request.FILES or None) #request FILES
        if form.is_valid():
            data = form.cleaned_data
            color.name = data['name']
            color.image = data['image']
            color.save()
            return redirect('color')
    return render(request, 'cloth/colorEdit.html', context={'color':color,'form':form})

@group_required('manager')
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

@group_required('manager')
def stockEdit(request, sid):
    cloth = Cloth_in_stock.objects.get(pk=sid)
    form = Cloth_in_stockForm(instance=cloth)
    if request.method == 'POST':
        form = Cloth_in_stockForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cloth.quantity = data['quantity']
            cloth.cloth_type = data['cloth_type']
            cloth.color = data['color']
            cloth.price = data['price']
            cloth.save()
            return redirect('stock')
    return render(request, 'cloth/stockEdit.html', context={'form':form, 'cloth':cloth})
