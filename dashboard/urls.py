from django.urls import path
from .views import cashier, dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('pos/', cashier, name='cashier'),
]
