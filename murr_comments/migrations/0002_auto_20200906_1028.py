# Generated by Django 3.0.8 on 2020-09-06 05:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('murr_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='disliked_murrens',
            field=models.ManyToManyField(related_name='disliked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='liked_murrens',
            field=models.ManyToManyField(related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(blank=True, default=0, verbose_name='Рейтинг'),
        ),
    ]
