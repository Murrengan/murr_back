from django.urls import path
from .views import MurrCardView


urlpatterns = [
    path('', MurrCardView.as_view(), name='MurrCardView'),

]
