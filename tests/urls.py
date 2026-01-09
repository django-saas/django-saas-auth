from django.urls import path, include
from saas_base.endpoints.user import UserEndpoint

urlpatterns = [
    path('api/user/', UserEndpoint.as_view()),
    path('api/user/profile/', include('saas_auth.api_urls.user')),
    path('api/user/sessions/', include('saas_auth.api_urls.session')),
    path('api/user/tokens/', include('saas_auth.api_urls.token')),
]
