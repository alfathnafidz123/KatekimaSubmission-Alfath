from rest_framework import serializers
from .models import Item, PurchaseHeader, PurchaseDetail, SellHeader, SellDetail


class ItemSerializer(serializers.ModelSerializer):
    # Serializer untuk model Item

    class Meta:
        model = Item
        fields = '__all__'  # Gunakan semua field dari model


class PurchaseDetailSerializer(serializers.ModelSerializer):
    #Serializer untuk detail pembelian

    class Meta:
        model = PurchaseDetail
        fields = '__all__'


class PurchaseHeaderSerializer(serializers.ModelSerializer):
    #Serializer untuk header pembelian termasuk detailnya
    details = PurchaseDetailSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = PurchaseHeader
        fields = '__all__'


class SellDetailSerializer(serializers.ModelSerializer):
    # Serializer untuk detail penjualan

    class Meta:
        model = SellDetail
        fields = '__all__'


class SellHeaderSerializer(serializers.ModelSerializer):
    #Serializer untuk header penjualan termasuk detailnya
    details = SellDetailSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = SellHeader
        fields = '__all__'