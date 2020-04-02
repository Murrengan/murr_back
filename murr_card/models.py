from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models

Murren = get_user_model()


class MurrCard(models.Model):
    title = models.CharField(max_length=224)
    cover = models.ImageField(blank=True, null=True, upload_to='murr_cover/%Y/%m/%d/')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Murren, on_delete=models.CASCADE, related_name='murr_cards')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover:

            img = Image.open(self.cover.path)

            if img.mode in ('RGBA', 'LA'):
                fill_color = '#A36FFF'
                background = Image.new(img.mode[:-1], img.size, fill_color)
                background.paste(img, img.split()[-1])
                img = background

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.cover.path)


class EditorImageForMurrCard(models.Model):
    murr_editor_image = models.ImageField(upload_to='editor_image_for_murr_card/%Y/%m/%d/', null=True, max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.murr_editor_image.path)
        img = img.convert('RGB')

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.murr_editor_image.path)
