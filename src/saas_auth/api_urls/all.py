from django.urls import path, include

urlpatterns = [
    path('profile/', include('saas_auth.api_urls.profile')),
    path('sessions/', include('saas_auth.api_urls.session')),
    path('tokens/', include('saas_auth.api_urls.token')),
]
