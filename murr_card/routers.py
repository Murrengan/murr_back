from rest_framework import routers
from .views import MurrCardView

router = routers.SimpleRouter()
router.register('', MurrCardView, basename='')
