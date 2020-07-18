# Generated by Django 3.0.3 on 2020-06-30 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MurrChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('murr_chat_name', models.CharField(max_length=244)),
            ],
        ),
        migrations.CreateModel(
            name='MurrChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='')),
                ('chat_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='murr_chat_message', to='murr_chat.MurrChat')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='murren_message', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MurrChatMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='murr_chat_member', to='murr_chat.MurrChat')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='murr_chat_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]