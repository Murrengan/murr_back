from django.db import models

from murren.models import Murren


class Rating(models.Model):
    murren = models.ForeignKey(Murren, verbose_name='Муррен', related_name='ratings', on_delete=models.CASCADE)
    rating_type = models.CharField('Тип оценки', max_length=4, null=True, blank=True)
    object_id = models.PositiveIntegerField('Идентификатор объекта')
    object_type = models.CharField('Тип объекта', max_length=255)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
