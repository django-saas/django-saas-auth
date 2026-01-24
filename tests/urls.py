from django.urls import include, path
from drf_spectacular.views import SpectacularJSONAPIView

urlpatterns = [
    path('api/user/', include('saas_auth.api_urls.all')),
    path('schema/openapi', SpectacularJSONAPIView.as_view(), name='schema'),
]
