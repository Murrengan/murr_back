from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from .views import MurrCardView, EditorImageForMurrCardView, AllMurr, Search

urlpatterns = [
    path('', csrf_exempt(MurrCardView.as_view()), name='MurrCardView'),
    path('save_editor_image/', csrf_exempt(EditorImageForMurrCardView.as_view()), name='save_editor_image'),
    path('all/', csrf_exempt(AllMurr.as_view()), name='all_murrr'),
    path('murr/', csrf_exempt(Search.as_view()), name='search_murr'),
]
