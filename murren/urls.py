from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MurrensMethods, GetAllMurrens, PublicMurrenInfo, GetTanochkaImg, TokenCheck, MyTokenObtainPairView, \
    TokenGenerate

urlpatterns = [
    path('', MurrensMethods.as_view(), name='MurrensMethods'),
    path('tanochka/', GetTanochkaImg.as_view(), name='get_tanochka_img'),
    path('all/', GetAllMurrens.as_view(), name='get_all_murrens'),
    path('<int:pk>/', PublicMurrenInfo.as_view(), name='get_murren_info_by_pk'),

    path('token_check/', TokenCheck.as_view(), name='token_check'),
    path('token_generate/', TokenGenerate.as_view(), name='token_generate'),

    path('token_create/', MyTokenObtainPairView.as_view(), name='obtain_token_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
