from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from murren.models import Murren
from murr_card.models import MurrCard
from murr_rating.models import RatingAbstractModel


class Comment(RatingAbstractModel, MPTTModel):
    author = models.ForeignKey(Murren, verbose_name='Автор', related_name='comments', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    murr = models.ForeignKey(MurrCard, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField('Комментарий')
    created = models.DateTimeField('Дата написания', auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    class MPTTMeta:
        order_insertion_by = ['-rating', '-created']
