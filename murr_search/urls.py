from django.urls import path


urlpatterns = [
    path('', SearchResultsView.as_view(), name='search'),
]