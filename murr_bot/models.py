from django.db import models


class Coub(models.Model):
    title = models.TextField()
    likes_count = models.IntegerField()
    url = models.TextField()
    search_phrase = models.TextField()

    def __str__(self):
        return self.title
