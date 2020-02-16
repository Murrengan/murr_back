from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # local
    path('murren/', include('murren.urls')),
    path('murr_card/', include('murr_card.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
