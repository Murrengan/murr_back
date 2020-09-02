from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'murr', 'parent')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.get_response(queryset)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve all descendants of object
        """
        instance = self.get_object()
        queryset = Comment.objects.get_queryset_descendants(Comment.objects.filter(id=instance.id), include_self=True)\
            .select_related('author', 'murr', 'parent')
        return self.get_response(queryset)

    def get_response(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(cache_tree_children(page), many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(cache_tree_children(queryset), many=True)
        return Response(serializer.data)
