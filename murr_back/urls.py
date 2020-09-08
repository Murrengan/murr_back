from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(title="Murrengan Schema API", default_version='v1'),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin_panel_secure_url/', admin.site.urls),

    # 3rd party
    path('auth/', include('djoser.urls')),

    # local
    path('api/murren/', include('murren.urls')),
    path('api/murr_card/', include('murr_card.urls')),
    path('api/murr_comments/', include('murr_comments.urls')),
    path('api/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)