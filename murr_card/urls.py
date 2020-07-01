from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import MurrCardView, EditorImageForMurrCardView, AllMurr, CommentView

urlpatterns = [
    path('', csrf_exempt(MurrCardView.as_view()), name='MurrCardView'),
    path('save_editor_image/', csrf_exempt(EditorImageForMurrCardView.as_view()), name='save_editor_image'),
    path('all/', csrf_exempt(AllMurr.as_view()), name='all_murrr'),

    # CRUD for comments
    path('comments/', CommentView.as_view(), name='CommentView')
]
