
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),

    path('dashboard/', include('dashboard.urls')),
    path('products/', include('products.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'api/',
        include('api.urls')
    ),
    path(
        'analytics/',
        include('analytics.urls')
    ),
    path(

        'api/mobile/',

        include(

            'mobile.urls'

        )

    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
