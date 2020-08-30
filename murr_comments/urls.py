from rest_framework import routers

from .views import CommentViewSet


router = routers.DefaultRouter()
router.register('', CommentViewSet, basename='comment')

urlpatterns = router.urls