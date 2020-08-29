from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import MurrensMethods, GetAllMurrens, PublicMurrenInfo, GetTanochkaImg, GoogleLogin

urlpatterns = [
    path('', MurrensMethods.as_view(), name='MurrensMethods'),
    path('tanochka/', GetTanochkaImg.as_view(), name='get_tanochka_img'),
    path('all/', GetAllMurrens.as_view(), name='get_all_murrens'),
    path('<int:pk>/', PublicMurrenInfo.as_view(), name='get_murren_info_by_pk'),

    url('token_create/', obtain_jwt_token),
    path('oauth/google/', GoogleLogin.as_view(), name='google_login')

]
