from rest_framework import serializers
from products.models import Product
from sales.models import Customer, POSSale, POSSaleItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id',
            'customer_code',
            'name',
            'phone',
            'email',
            'current_balance',
            'is_active',
        )


class POSSaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = POSSaleItem
        fields = (
            'id',
            'product',
            'product_name',
            'quantity',
            'unit_price',
        )


class POSSaleSerializer(serializers.ModelSerializer):
    items = POSSaleItemSerializer(source='possaleitem_set', many=True, read_only=True)

    class Meta:
        model = POSSale
        fields = (
            'id',
            'sale_number',
            'customer',
            'warehouse',
            'cashier',
            'total_amount',
            'sale_date',
            'items',
        )
        read_only_fields = (
            'id',
            'sale_number',
            'warehouse',
            'cashier',
            'sale_date',
            'items',
        )
