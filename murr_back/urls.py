from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin_panel_secure_url/', admin.site.urls),
    path('api/doc/', get_swagger_view(title="Murrengan network API")),
    # 3rd party
    path('auth/', include('djoser.urls')),

    # local
    path('api/murren/', include('murren.urls')),
    path('api/murr_card/', include('murr_card.urls')),
    path('api/murr_comments/', include('murr_comments.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)