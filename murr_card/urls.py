from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from .views import MurrCardViewSet, EditorImageForMurrCardView, MurrCardSearch

router = DefaultRouter()
router.register('', MurrCardViewSet, basename='murr_card')

urlpatterns = [
    path('save_editor_image/', csrf_exempt(EditorImageForMurrCardView.as_view()), name='save_editor_image'),
    path('search/', MurrCardSearch.as_view(), name='search')
]

urlpatterns += router.urls
