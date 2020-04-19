from rest_framework import serializers
from cloth.models import Cloth_in_stock, Cloth_type, Color
from account.models import Sell_list, Engage_list


class Sell_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell_list
        exclude = ['selling_revenue', 'cloth_in_stock']
        
class Engage_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engage_list
        exclude = ['engaging_revenue', 'list_no', 'cloth_type', 'color']

class Cloth_in_stockSerializer(serializers.ModelSerializer):
    cloth_sell = Sell_listSerializer(many=True, read_only=True)
    class Meta:
        model = Cloth_in_stock
        fields = ['quantity', 'price', 'cloth_sell']

class Cloth_typeSerializer(serializers.ModelSerializer):
    cloth_stock = Cloth_in_stockSerializer(many=True, read_only=True)
    cloth_engage = Engage_listSerializer(many=True, read_only=True)
    class Meta:
        model = Cloth_type
        fields = ['name', 'cloth_desc', 'cloth_stock', 'cloth_engage']

class ColorSerializer(serializers.ModelSerializer):
    color_stock = Cloth_in_stockSerializer(many=True, read_only=True)
    color_engage = Engage_listSerializer(many=True, read_only=True)
    class Meta:
        model = Color
        fields = ['name', 'image', 'color_stock', 'color_engage']
