from rest_framework import serializers

from .models import MurrCard, EditorImageForMurrCard


class MurrCardSerializers(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    owner_url = serializers.ReadOnlyField(source='owner.murren_url')

    class Meta:
        model = MurrCard
        fields = ('owner', 'title', 'cover', 'content', 'id', 'owner_name', 'owner_url')
        read_only_fields = ('owner_url', )


class EditorImageForMurrCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditorImageForMurrCard
        fields = ('murr_editor_image',)


class AllMurrSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MurrCard
        fields = ('id', 'title', 'cover', 'owner_name')
