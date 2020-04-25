from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cloth.models import Cloth_in_stock, Cloth_type, Color
from account.models import Revenue, Engaging, Sell_list, Selling, Engage_list
from django.db.models import Sum
from project.check import group_required
import json
from django.db.models import Max, Min #Models.objects.all().aggregate(Avg('price'))
from rest_framework.renderers import JSONRenderer
from ceo.serializers import Cloth_typeSerializer, ColorSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@group_required('ceo')
def index(request):
    context = {}
    return render(request, 'ceo/index.html', context=context)

@group_required('ceo')
def graph(request):
    context = {}
    return render(request, 'ceo/graph.html', context=context)
    
@group_required('ceo')
def clothList(request, name): #send API Data
    cloth = Cloth_type.objects.all()
    color = Color.objects.all()
    if request.method == 'GET':
        if name == 'color':
            serializer = ColorSerializer(instance=color, many=True)
        elif name == 'cloth':
            serializer = Cloth_typeSerializer(instance=cloth, many=True)
    return JsonResponse(serializer.data, safe=False)
