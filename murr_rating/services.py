from django.db.models import OuterRef
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from murr_rating.models import Rating


class RatingActionsMixin:

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        instance = self.get_object()
        object_type = instance.__class__.__name__
        rating_handler(request.user.id, instance.id, object_type, 'Like')
        return Response(status=200)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        instance = self.get_object()
        object_type = instance.__class__.__name__
        rating_handler(request.user.id, instance.id, object_type, 'Dislike')
        return Response(status=200)


def get_rating_query(object_type: str) -> tuple:
    """
    Get queryset's for an aggregate function to count difference between likes and dislikes
    """
    rating = Rating.objects.filter(object_id=OuterRef('pk'), object_type=object_type).only('pk')
    likes = rating.filter(rating_type='Like')
    dislikes = rating.filter(rating_type='Dislike')
    return likes, dislikes


def rating_handler(murren_id: int, obj_id: int, obj_type: str, rating_type: str) -> None:
    """
    Rating logic handler
    1. Get or create rating instance
    2. If not is_created and instance.rating_type == rating_type: instance.delete() (cancel action)
       Otherwise rating instance will save with rating_type
    """
    rating, is_created = Rating.objects.get_or_create(murren_id=murren_id, object_id=obj_id, object_type=obj_type)
    if not is_created and rating.rating_type == rating_type:
        rating.delete()
    else:
        rating.rating_type = rating_type
        rating.save()
