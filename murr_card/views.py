import base64
import logging

from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from url_filter.integrations.drf import DjangoFilterBackend

from murr_back.settings import LOCALHOST
from .models import MurrCard
from .serializers import MurrCardSerializers, EditorImageForMurrCardSerializers

logger = logging.getLogger(__name__)


class MurrCardView(ModelViewSet):
    serializer_class = MurrCardSerializers
    queryset = MurrCard.objects.all().order_by('-timestamp')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'owner', 'title', 'cover', 'content', 'id',
    )

    def perform_create(self, serializer):
        if serializer.data.get('cover'):
            content = serializer.data['cover']
            _, img_str = content.split('base64,')
            image_extension = _.split('/')[-1].split(';')[0]
            img_base64 = base64.b64decode(img_str)
            image_b = ContentFile(img_base64)
            image_b.name = get_random_string(length=6) + '.' + image_extension
            serializer.data['cover'] = image_b

        return serializer.save(owner=serializer.user.id)

    def destroy(request, *args, **kwargs):
        murr = MurrCard.objects.get(id=request.data['murr_id'])
        owner = murr.owner.id
        logged_user = request.user.id
        if owner == logged_user:
            murr.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EditorImageForMurrCardView(APIView):
    permission_classes = (IsAuthenticated,)

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
