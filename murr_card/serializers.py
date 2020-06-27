from rest_framework import serializers

from comments.serializers import CommentSerializer
from .models import MurrCard, EditorImageForMurrCard


class MurrCardSerializers(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True)

    class Meta:
        model = MurrCard
        fields = ('owner', 'title', 'cover', 'content', 'id', 'owner_name', 'comments')


class EditorImageForMurrCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = EditorImageForMurrCard
        fields = ('murr_editor_image',)


class AllMurrSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MurrCard
        fields = ('owner_name', 'title', 'cover', 'id')
