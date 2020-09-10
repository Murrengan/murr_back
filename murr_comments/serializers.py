from rest_framework import serializers


from .models import Comment


class ChildSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_username', 'parent', 'murr', 'text', 'rating', 'created', 'children')
        read_only_fields = ('rating', 'created')

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_username', 'parent', 'murr', 'text', 'rating', 'created', 'children')
        read_only_fields = ('rating', 'created')
