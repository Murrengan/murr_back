from rest_framework import serializers


from .models import Comment


class ChildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.username')
    murr_id = serializers.CharField(source='murr.id')
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'parent', 'murr_id', 'text', 'created', 'children')

    def get_children(self, parent):
        queryset = parent.get_children()
        serialized_data = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serialized_data.data


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(label='Автор')
    author_username = serializers.CharField(source='author.username', read_only=True)
    parent_id = serializers.IntegerField(label='Родитель')
    murr_id = serializers.IntegerField(label='Мурр кард')
    created = serializers.DateTimeField(read_only=True)
    children = serializers.SerializerMethodField()

    def get_children(self, parent):
        queryset = parent.get_children()
        serialized_data = ChildSerializer(queryset, many=True, read_only=True, context=self.context)
        return serialized_data.data

    class Meta:
        model = Comment
        fields = ('id', 'author_id', 'author_username', 'parent_id', 'murr_id', 'text', 'created', 'children')