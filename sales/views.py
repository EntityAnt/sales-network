from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from users.permissions import IsActiveUser

from .models import Contacts, NetworkNode, Product
from .paginations import SalesPagination
from .serializers import ContactsSerializer, NetworkNodeSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = SalesPagination
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "model"]

    def perform_create(self, serializer):
        # Передаем текущего пользователя в сериализатор
        serializer.save(user=self.request.user)


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    pagination_class = SalesPagination
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country", "city"]

    def perform_create(self, serializer):
        # Передаем текущего пользователя в сериализатор
        serializer.save(user=self.request.user)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    pagination_class = SalesPagination
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["contacts__country"]  # Фильтрация по стране
    ordering_fields = ["name", "created_at"]  # Сортировка по имени и дате создания
    search_fields = ["name"]  # Поиск по имени

    def perform_create(self, serializer):
        # Передаем текущего пользователя в сериализатор
        serializer.save(user=self.request.user)
