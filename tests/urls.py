from django.urls import path, include

urlpatterns = [
    path('api/user/', include('saas_auth.api_urls.all')),
]
