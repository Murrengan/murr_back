from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.contrib.auth import get_user_model
from rest_auth.registration.views import SocialLoginView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from murren.permissions import MurrenPermission
from murren.serializers import MurrenSerializers, PublicMurrenInfoSerializers

Murren = get_user_model()


class MurrensMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        r = Murren.objects.get(id=request.user.id)
        data = {'murren_name': r.username}
        return Response(data)


class GetTanochkaImg(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'img_url': '/media/tanochka.jpg'}
        return Response(data)


class PublicMurrenInfo(APIView):

    def get(self, request, pk):
        r = Murren.objects.get(id=pk)
        serializer = PublicMurrenInfoSerializers(r, context={'request': request})
        return Response(serializer.data)


class GetAllMurrens(ListAPIView):
    queryset = Murren.objects.filter(is_active=True).order_by('-date_joined')
    serializer_class = MurrenSerializers
    pagination_class = PageNumberPagination


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class MurrenPermissionMixin:
    murren_permission = MurrenPermission()
