from django.urls import path

from comments.views import CommentView

urlpatterns = [
    # CRUD
    path('', CommentView.as_view(), name='CommentView')
    # Create
    # path('create/', ...),
    # Read,
    # path('', ...),
    # Update
    # path('', ...),
    # Delete
    # path('', ...)
]