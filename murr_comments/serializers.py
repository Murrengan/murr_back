from rest_framework import serializers


from .models import Comment


class ChildSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()
    rating = serializers.IntegerField(label='Рейтинг', default=0, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_username', 'parent', 'murr', 'text', 'created', 'rating', 'children')

    def get_children(self, parent):
        queryset = parent.get_children()
        serialized_data = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serialized_data.data


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()
    rating = serializers.IntegerField(label='Рейтинг', default=0, read_only=True)

    def get_children(self, parent):
        queryset = parent.get_children()
        serialized_data = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serialized_data.data

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_username', 'parent', 'murr', 'text', 'created', 'rating', 'children')
