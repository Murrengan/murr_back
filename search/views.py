from rest_framework.generics import ListAPIView
from murr_card.serializers import AllMurrSerializer
from murr_card.models import MurrCard
from murr_card.views import MurrPagination
from django_filters import rest_framework as rest_filter
from rest_framework import filters



class Search(ListAPIView):
    queryset = MurrCard.objects.all()
    serializer_class = AllMurrSerializer
    pagination_class = MurrPagination
    filter_backends = (rest_filter.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['title']


