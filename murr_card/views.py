import base64
import logging

from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from murr_back.settings import LOCALHOST
from .models import MurrCard
from .serializers import (MurrCardSerializers, EditorImageForMurrCardSerializers, AllMurrSerializer,
                          AllMurrShortSerializer,
                          )

logger = logging.getLogger(__name__)


class MurrCardView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        qs = MurrCard.objects.filter(id=request.query_params['murr_id'])
        serializer = MurrCardSerializers(qs, many=True)
        return Response(serializer.data)

    def post(self, request):

        if request.data.get('cover'):
            content = request.data['cover']
            _, img_str = content.split('base64,')
            image_extension = _.split('/')[-1].split(';')[0]
            img_base64 = base64.b64decode(img_str)
            image_b = ContentFile(img_base64)
            image_b.name = get_random_string(length=6) + '.' + image_extension
            request.data['cover'] = image_b

        request.data['owner'] = request.user.id

        serializer = MurrCardSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EditorImageForMurrCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = EditorImageForMurrCardSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            url = LOCALHOST + serializer.data['murr_editor_image']
            murr_dict = {"success": 1, "file": {"url": url}}

            return Response(murr_dict)

        else:

            murr_dict = {"success": 0, "file": {"url": ""}}
            return Response(murr_dict)


class MurrPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'murr_card_len'
    max_page_size = 60


class AllMurr(ListAPIView):
    pagination_class = MurrPagination

    def get_serializer_class(self):
        murren_id = self.request.query_params.get('murren_id')
        if murren_id:
            return AllMurrShortSerializer
        return AllMurrSerializer

    def get_queryset(self):
        murren_id = self.request.query_params.get('murren_id')
        queryset = MurrCard.objects.all().order_by('-timestamp')
        if murren_id:
            queryset = queryset.filter(owner_id=murren_id)
            return queryset
        return queryset
