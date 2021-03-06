# Generated by Django 3.0.3 on 2020-04-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EditorImageForMurrCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('murr_editor_image', models.ImageField(max_length=255, null=True, upload_to='editor_image_for_murr_card/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='MurrCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=224)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='murr_cover/%Y/%m/%d/')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
