from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sales.apps import SalesConfig

from .views import ContactsViewSet, NetworkNodeViewSet, ProductViewSet

app_name = SalesConfig.name

router = DefaultRouter()
router.register(r"suppliers", NetworkNodeViewSet, basename="supplier")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"contacts", ContactsViewSet, basename="contact")

urlpatterns = [
    path("", include(router.urls)),
]
