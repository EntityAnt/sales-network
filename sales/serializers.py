from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Contacts, NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date", "user"]
        read_only_fields = ["user"]  # Поле user не может быть изменено через API

    def create(self, validated_data):
        # Автоматически добавляем текущего пользователя
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ["id", "email", "country", "city", "street", "house_number", "user"]
        read_only_fields = ["user"]  # Поле user не может быть изменено через API

    def create(self, validated_data):
        # Автоматически добавляем текущего пользователя
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    contacts = ContactsSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "type",
            "contacts",
            "products",
            "supplier",
            "debt",
            "created_at",
            "user",
        ]
        read_only_fields = ["debt", "user"]  # Запрещаем обновление полей debt и user

    def create(self, validated_data):
        # Автоматически добавляем текущего пользователя
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
