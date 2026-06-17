from django.shortcuts import render

# Create your views here.
from .dashboards import executive_dashboard


def executive_dashboard_view(request):

    context = executive_dashboard()

    return render(

        request,

        'analytics/dashboard.html',

        context

    )
