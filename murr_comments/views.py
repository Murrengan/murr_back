from django.db.models import Count, Subquery


from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from mptt.templatetags.mptt_tags import cache_tree_children


from .models import Comment
from .serializers import CommentSerializer

from murr_rating.services import RatingActionsMixin, get_rating_query


class CommentViewSet(RatingActionsMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('murr', 'parent', 'author')

    def get_queryset(self):
        likes, dislikes = get_rating_query('Comment')
        queryset = cache_tree_children(Comment.objects.select_related('author', 'murr', 'parent').annotate(
            rating=Count(Subquery(likes)) - Count(Subquery(dislikes))
        ))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.get_response(queryset)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve object and all of its descendants
        """
        instance = self.get_object()
        queryset = Comment.objects\
            .get_queryset_descendants(Comment.objects.filter(id=instance.id), include_self=True)\
            .select_related('author', 'murr', 'parent')
        return self.get_response(queryset)

    def get_response(self, queryset):
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(cache_tree_children(page), many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(cache_tree_children(queryset), many=True)
        return Response(serializer.data)
