# Generated by Django 3.0.8 on 2020-09-07 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('murr_comments', '0002_auto_20200906_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1500, verbose_name='Комментарий'),
        ),
    ]
