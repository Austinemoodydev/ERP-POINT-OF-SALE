from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from inventory.models import Warehouse
from products.models import Product
from sales.models import Customer, POSSale, POSSaleItem

from .serializers import CustomerSerializer, POSSaleSerializer, ProductSerializer


class POSSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return super().enforce_csrf(request)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication, POSSessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand', 'unit')
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'sku', 'barcode')

    def get_queryset(self):
        queryset = super().get_queryset()
        barcode = self.request.query_params.get('barcode')
        category = self.request.query_params.get('category')

        if barcode:
            queryset = queryset.filter(barcode=barcode)
        if category:
            queryset = queryset.filter(category_id=category)

        return queryset


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication, POSSessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'phone', 'customer_code', 'email')

    def get_queryset(self):
        return Customer.objects.filter(is_active=True).order_by('name')


class POSSaleViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication, POSSessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = POSSaleSerializer
    http_method_names = ('get', 'post', 'head', 'options')

    def get_queryset(self):
        return (
            POSSale.objects
            .filter(cashier=self.request.user)
            .select_related('customer', 'warehouse', 'cashier')
            .prefetch_related('possaleitem_set__product')
            .order_by('-sale_date')
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart_items = request.data.get('items') or []
        if not cart_items:
            return Response(
                {'detail': 'Cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        warehouse = self._get_warehouse(request.data.get('warehouse'))
        if warehouse is None:
            return Response(
                {'detail': 'Create at least one warehouse before completing POS sales.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = self._get_customer(request.data.get('customer'))
        sale_number = self._sale_number()
        total = Decimal('0.00')
        prepared_items = []

        for item in cart_items:
            product_id = item.get('product') or item.get('id')
            try:
                product = Product.objects.get(pk=product_id, is_active=True)
                quantity = Decimal(str(item.get('quantity') or item.get('qty') or 1))
                unit_price = Decimal(str(item.get('unit_price') or item.get('price') or product.selling_price))
            except (Product.DoesNotExist, InvalidOperation, TypeError, ValueError):
                return Response(
                    {'detail': 'One or more cart items are invalid.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if quantity <= 0 or unit_price < 0:
                return Response(
                    {'detail': 'Item quantities and prices must be valid positive values.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total += quantity * unit_price
            prepared_items.append((product, quantity, unit_price))

        discount = self._decimal(request.data.get('discount'), default='0.00')
        vat = self._decimal(request.data.get('vat'), default='0.00')
        total_amount = max(Decimal('0.00'), total - discount) + vat

        sale = POSSale.objects.create(
            sale_number=sale_number,
            customer=customer,
            warehouse=warehouse,
            cashier=request.user,
            total_amount=total_amount,
        )

        POSSaleItem.objects.bulk_create(
            POSSaleItem(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
            )
            for product, quantity, unit_price in prepared_items
        )

        serializer = self.get_serializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_customer(self, customer_id):
        if not customer_id:
            return None
        try:
            return Customer.objects.get(pk=customer_id, is_active=True)
        except (Customer.DoesNotExist, TypeError, ValueError):
            return None

    def _get_warehouse(self, warehouse_id):
        if warehouse_id:
            try:
                return Warehouse.objects.get(pk=warehouse_id, is_active=True)
            except (Warehouse.DoesNotExist, TypeError, ValueError):
                return None

        return Warehouse.objects.filter(is_active=True).order_by('id').first()

    def _sale_number(self):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
        return f'POS-{timestamp}'

    def _decimal(self, value, default='0.00'):
        try:
            return Decimal(str(value if value is not None else default))
        except (InvalidOperation, TypeError, ValueError):
            return Decimal(default)
