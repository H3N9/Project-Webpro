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

class ColorForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='รูปสี')
    class Meta:
        model = models.Color
        fields = '__all__'
        labels = {
            'name':'สี',
        }
class Cloth_in_stockForm(forms.ModelForm):
    class Meta:
        model = models.Cloth_in_stock
        fields = '__all__'
