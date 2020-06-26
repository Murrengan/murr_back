from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import Search

urlpatterns = [
    path('', csrf_exempt(Search.as_view()), name='search_murr'),
]
