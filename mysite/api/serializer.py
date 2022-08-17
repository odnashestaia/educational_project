from rest_framework import serializers

from demo.models import Product, Basket


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'category', 'name']


class CartSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Basket
        fields = ['id', 'product', 'count']
