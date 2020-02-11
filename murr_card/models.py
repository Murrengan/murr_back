from django.contrib.auth import get_user_model
from django.db import models


Murren = get_user_model()


class MurrCard(models.Model):

    title = models.CharField(max_length=128)
    cover = models.ImageField(blank=True, upload_to='murren_pics')
    description = models.CharField(max_length=256)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Murren, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
