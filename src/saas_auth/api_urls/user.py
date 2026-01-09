from django.urls import path
from ..endpoints.profile import UserProfileEndpoint


urlpatterns = [
    path('', UserProfileEndpoint.as_view()),
]
