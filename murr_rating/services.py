from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RatingActionsMixin:

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        rating_handler(request.user, instance, instance.liked_murrens, instance.disliked_murrens)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        rating_handler(request.user, instance, instance.disliked_murrens, instance.liked_murrens)
        return Response(serializer.data)


def rating_handler(murren, instance, current, other):
    """
    current, other - actions (like or dislike)
    if current already exists: remove it (cancel action).
    otherwise add a request user to current action. other remove.
    """
    current_exists = current.filter(id=murren.id).first()
    other_exists = other.filter(id=murren.id).first()

    current.remove(murren) if current_exists else current.add(murren)
    other.remove(murren) if other_exists else None

    instance.rating = instance.liked_murrens.count() - instance.disliked_murrens.count()
    instance.save()
