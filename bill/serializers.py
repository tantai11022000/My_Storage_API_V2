from dataclasses import fields
from rest_framework import serializers
from .models import Bill,BillDetail
from storage.models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['name']


class BillDetailSerializer(serializers.ModelSerializer):
    codeGood = GoodsSerializer()
    class Meta:
        model = BillDetail
        fields = ['codeGood','amount','price']

class BillSerializer(serializers.ModelSerializer):
    bill_detail = BillDetailSerializer(many=True)
    class Meta:
        model = Bill
        fields = '__all__'

class NewBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class NewBillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = '__all__'

