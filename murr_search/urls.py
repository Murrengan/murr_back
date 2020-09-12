from django.urls import path

from murr_search.views import SearchMurrenView, SearchMurrCardView

urlpatterns = [
    path('murren/', SearchMurrenView.as_view(), name='search_murren'),
    path('murr_card/', SearchMurrCardView.as_view(), name='search_murr_card'),

]
