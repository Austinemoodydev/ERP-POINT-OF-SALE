from django.urls import path
from .views import executive_dashboard_view
urlpatterns = [

    path(
        '',
        executive_dashboard_view,
        name='executive_dashboard'
    )

]
