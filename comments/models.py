from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from murr_card.models import MurrCard
from murren.models import Murren


class Comment(models.Model):
    """ Модель комментнария для murr_card """
    murr_card = models.ForeignKey(MurrCard, on_delete=models.CASCADE, related_name='comments', verbose_name='murr_card')
    owner = models.ForeignKey(Murren, on_delete=models.CASCADE, related_name='comments',
                              verbose_name='Автор комментария')
    text = models.TextField(max_length=512)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name='Родительский комментарий', null=True)
    depth = models.IntegerField(verbose_name='Глубина комментария', default=1,
                                validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return f'{self.owner}: "{self.text}"'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
