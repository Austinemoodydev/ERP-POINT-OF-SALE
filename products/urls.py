from django.urls import path
from . import views
urlpatterns = [
    path(

        'scan/',

        views.scan_barcode,

        name='scan_barcode'

    )
]
