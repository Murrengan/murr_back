from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer
from murr_card.models import MurrCard


class CommentView(APIView):

    def get(self, request):
        murr_card = MurrCard.objects.get(pk=request.query_params['murr_id'])
        comments = Comment.objects.filter(murr_card=murr_card)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        В запросе должен быть json вида
        {
            murr_card: ...,
            owner: ...,
            text: ...,
            parent: ...,
        }

        """
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            parent_comment = serializer.validated_data.get('parent')
            serializer.validated_data['depth'] = parent_comment.depth + 1
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        pk = request.query_params['comment_id']
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        data = request.data
        serializer = CommentSerializer(instance=comment, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        pk = request.query_params['comment_id']
        comment = get_object_or_404(Comment.objects.all(), pk=pk)
        comment.delete()
        return Response(
            {
                'success': True,
                'message': f'Comment with id {pk} has been deleted'
            }, status=204
        )
