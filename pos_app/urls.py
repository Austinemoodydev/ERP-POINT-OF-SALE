from django.urls import path
from . import views

app_name = "pos_app"

urlpatterns = [
    path("",               views.pos_dashboard, name="dashboard"),
    path("complete-sale/", views.complete_sale,  name="complete_sale"),
    path("shift/open/",    views.shift_open,     name="shift_open"),
    path("shift/close/",   views.shift_close,    name="shift_close"),
    path("drawer/open/",   views.drawer_open,    name="drawer_open"),
    path("drawer/deposit/",views.drawer_deposit, name="drawer_deposit"),
]
