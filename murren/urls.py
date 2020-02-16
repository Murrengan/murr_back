from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# 3rd party
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# local
from .views import MurrensMethods, murren_register, murren_activate, GetAllMurrens, PublicMurrenInfo, GetTanochkaImg, \
    reset_password, confirm_new_password

urlpatterns = [
    path('', MurrensMethods.as_view(), name='MurrensMethods'),
    path('tanochka/', GetTanochkaImg.as_view(), name='get_tanochka_img'),
    path('all/', GetAllMurrens.as_view(), name='get_all_murrens'),
    path('<int:pk>/', PublicMurrenInfo.as_view(), name='get_murren_info_by_pk'),

    # rest
    path('register/', csrf_exempt(murren_register), name='murren_register'),
    path('activation/', csrf_exempt(murren_activate), name='murren_activate'),
    path('reset_password/', csrf_exempt(reset_password), name='reset_password'),
    path('confirm_new_password/', csrf_exempt(confirm_new_password), name='confirm_new_password'),

    # 3rd party
    path('token_create/', TokenObtainPairView.as_view(), name='obtain_token_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
