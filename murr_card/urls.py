from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import EditorImageForMurrCardView
from .routers import router

urlpatterns = [
    path('save_editor_image/', csrf_exempt(EditorImageForMurrCardView.as_view()), name='save_editor_image'),
]
urlpatterns += router.urls
