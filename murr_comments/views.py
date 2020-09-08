from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment
from .services import CommentPagination
from .serializers import CommentSerializer
from murr_rating.services import RatingActionsMixin


class CommentViewSet(RatingActionsMixin, ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('murr', 'parent', 'author')

    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'murr', 'parent')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.get_cached_response(queryset)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve object and all of its descendants
        """
        instance = self.get_object()
        queryset = Comment.objects\
            .get_queryset_descendants(Comment.objects.filter(id=instance.id), include_self=True)\
            .select_related('author', 'murr', 'parent')
        return self.get_cached_response(queryset)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_cached_response(self, queryset):
        page = self.paginate_queryset(queryset.get_cached_trees())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
