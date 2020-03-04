from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class Murren(AbstractUser):

    email = models.EmailField(unique=True)
    murren_avatar = models.ImageField(default='default_murren_avatar.png', upload_to='murren_pics/%Y/%m/%d/',
                                      verbose_name='Аватар Муррена')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.murren_avatar.path)

        if img.mode in ('RGBA', 'LA'):
            fill_color = '#A36FFF'
            background = Image.new(img.mode[:-1], img.size, fill_color)
            background.paste(img, img.split()[-1])
            img = background

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.murren_avatar.path)


class EmailToken(models.Model):
    murren = models.ForeignKey(Murren, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = ("token")
        verbose_name_plural = ("tokens")

    def __str__(self):
        return self.token
