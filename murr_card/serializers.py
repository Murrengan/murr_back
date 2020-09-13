from django_enum_choices.serializers import EnumChoiceModelSerializerMixin
from rest_framework import serializers

from .models import MurrCard, EditorImageForMurrCard


class MurrCardSerializers(EnumChoiceModelSerializerMixin, serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.ReadOnlyField(source='owner.murren_url')

    class Meta:
        model = MurrCard
        fields = ('id', 'owner', 'title', 'cover', 'content', 'rating', 'owner_name', 'owner_url', 'status')
        read_only_fields = ('owner_url', 'rating')


class EditorImageForMurrCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditorImageForMurrCard
        fields = ('murr_editor_image',)


class AllMurrSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MurrCard
        fields = ('id', 'title', 'cover', 'rating', 'timestamp', 'owner_name')
        read_only_fields = ('rating', 'timestamp')
