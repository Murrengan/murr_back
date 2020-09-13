from django.contrib import admin
from django_enum_choices.admin import EnumChoiceListFilter

from .models import MurrCard


@admin.register(MurrCard)
class MyModelAdmin(admin.ModelAdmin):
    list_filter = [('status', EnumChoiceListFilter)]
