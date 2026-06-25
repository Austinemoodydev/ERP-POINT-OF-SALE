from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, POSSaleViewSet, ProductViewSet

router = DefaultRouter()

router.register(
    'products',
    ProductViewSet,
    basename='product',
)
router.register(
    'customers',
    CustomerViewSet,
    basename='customer',
)
router.register(
    'pos-sales',
    POSSaleViewSet,
    basename='pos-sale',
)
urlpatterns = [

    path(
        '',
        include(router.urls)
    )

]
