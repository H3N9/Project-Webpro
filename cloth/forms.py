from django import forms
from . import models

class Cloth_typeForm(forms.ModelForm):
    class Meta:
        model = models.Cloth_type
        fields = '__all__'
        labels = {
            'name':'ชื่อผ้า',
            'cloth_desc':'รายละเอียดผ้า',
        }
        widgets = {
            'name':forms.DateInput(attrs={ 'class':'form-control'}),
            'cloth_desc':forms.Textarea(attrs={ 'class':'form-control', 'rows': '3'})
        }

class ColorForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='รูปสี')
    class Meta:
        model = models.Color
        fields = '__all__'
        labels = {
            'name':'สี',
        }
        widgets = {            
            'name':forms.DateInput(attrs={ 'class':'form-control'}),
        }
class Cloth_in_stockForm(forms.ModelForm):
    class Meta:
        model = models.Cloth_in_stock
        fields = '__all__'
        labels = {
            'quantity':'จำนวน',
            'cloth_type': 'ประเภทผ้า',
            'color': 'สี',
            'price': 'ราคา'            
        }
        widgets = {
            'quantity':forms.NumberInput(attrs={'class':'form-control','oninput':"positive(document.getElementById(\'id_quantity\'))"}),
            'cloth_type':forms.Select(attrs={'class':'form-control'}),
            'color':forms.Select(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control','oninput':"positive(document.getElementById(\'id_price\'))"}),
        }