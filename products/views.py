from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Product


def scan_barcode(request):

    code = request.GET.get('barcode')

    product = Product.objects.filter(



        barcode=code


    ).first()

    if product:

        return JsonResponse({



            'name': product.name,

            'price': str(product.selling_price),

            'stock': product.stock


        })

    return JsonResponse({


        'error': 'Not found'

    })
