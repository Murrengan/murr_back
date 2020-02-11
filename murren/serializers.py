from rest_framework import serializers
from .models import Murren


class MurrenSerializers(serializers.ModelSerializer):

    class Meta:
        model = Murren
        fields = ('id', 'username')


class PublicMurrenInfoSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Murren
        fields = ('id', 'username', 'email', 'murren_avatar')
