from django.db import models

from murren.models import Murren


class RatingAbstractModel(models.Model):
    liked_murrens = models.ManyToManyField(Murren, related_name='liked_%(class)ss', blank=True)
    disliked_murrens = models.ManyToManyField(Murren, related_name='disliked_%(class)ss', blank=True)
    rating = models.IntegerField('Рейтинг', blank=True, default=0)

    class Meta:
        abstract = True
