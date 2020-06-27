from django.db import models

class Comment(models.Model):
    """ Модель комментнария для murr_card """
    murr_card = models.ForeignKey(MurrCard, on_delete=models.CASCADE, related_name='comments', verbose_name='murr_card')
    owner = models.ForeignKey(Murren, on_delete=models.CASCADE, related_name='comments',
                              verbose_name='Автор комментария')
    text = models.TextField(max_length=512)

    def __str__(self):
        return f'{self.owner}: "{self.text}"'
