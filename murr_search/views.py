from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from murr_card.models import MurrCard
from murr_card.serializers import MurrCardSerializers
from murr_card.views import MurrPagination
from murren.models import Murren
from murren.serializers import PublicMurrenInfoSerializers


class SearchMurrenView(ListAPIView):
    search_fields = ['username']
    filter_backends = (SearchFilter,)
    queryset = Murren.objects.all()
    serializer_class = PublicMurrenInfoSerializers
    pagination_class = MurrPagination


class SearchMurrCardView(ListAPIView):
    search_fields = ['title']
    filter_backends = (SearchFilter,)
    queryset = MurrCard.objects.all()
    serializer_class = MurrCardSerializers
    pagination_class = MurrPagination

