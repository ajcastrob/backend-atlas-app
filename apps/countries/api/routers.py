from rest_framework.routers import DefaultRouter
from apps.countries.api.country_view import CountryViewSet


router = DefaultRouter()
router.register("countries", CountryViewSet)

urlpatterns = router.urls
