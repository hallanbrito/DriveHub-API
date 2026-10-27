from rest_framework.routers import DefaultRouter
from .views import SaleProposalViewSet
router = DefaultRouter()
router.register("proposals", SaleProposalViewSet, basename="proposal")
urlpatterns = router.urls
