from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MurrCardSerializers
from .models import MurrCard


class MurrCardView(APIView):

    def get(self, request):
        qs = MurrCard.objects.all()
        serializer = MurrCardSerializers(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MurrCardSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
