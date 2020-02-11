from rest_framework import serializers
from .models import MurrCard


class MurrCardSerializers(serializers.ModelSerializer):

    class Meta:
        model = MurrCard
        fields = ('title', 'description', 'owner', 'cover', 'content')
