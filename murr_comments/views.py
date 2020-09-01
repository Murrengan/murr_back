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
        return cache_tree_children(Comment.objects.select_related('murr', 'author', 'parent'))

    def retrieve(self, request, *args, **kwargs):
        """
        Получить комментарий и дерево всех его потомков
        """
        pk = kwargs.pop('pk')
        if not pk.isdigit():
            raise NotFound()

        queryset = cache_tree_children(
            Comment.objects.get_queryset_descendants(
                Comment.objects.filter(pk=pk), include_self=True
            ).select_related('author', 'murr', 'parent')
        )
        serializer = CommentSerializer(queryset, many=True)

        if not serializer.data:
            raise NotFound()
        return Response(serializer.data)
