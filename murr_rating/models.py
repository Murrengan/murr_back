from django.db import models

from murren.models import Murren


class RatingAbstractModel(models.Model):
    liked_murrens = models.ManyToManyField(Murren, related_name='liked_%(class)ss')
    disliked_murrens = models.ManyToManyField(Murren, related_name='disliked_%(class)ss')
    rating = models.IntegerField('Рейтинг', blank=True, default=0)

    class Meta:
        abstract = True
