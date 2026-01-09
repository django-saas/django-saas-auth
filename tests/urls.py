from django.urls import path, include
from saas_base.endpoints.user import UserEndpoint

urlpatterns = [
    path('api/user/', UserEndpoint.as_view()),
    path('api/user/', include('saas_auth.api_urls.all')),
]
