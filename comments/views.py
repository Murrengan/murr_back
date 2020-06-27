from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentView(APIView):

    def get(self, request):
        print(Comment.objects.all())
        comments = Comment.objects.filter(id=request.query_params['comment_id'])
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
