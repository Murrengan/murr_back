from django.urls import path

from comments.views import CommentView

urlpatterns = [
    # CRUD
    path('', CommentView.as_view(), name='CommentView')
]