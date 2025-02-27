from django.contrib import admin
from django.db.models import F
from django.urls import reverse
from django.utils.html import format_html

from .models import Contacts, NetworkNode, Product


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house_number")
    search_fields = ("email", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "level",
        "supplier_link",
        "debt",
        "city_filter",
        "created_at",
    )
    list_filter = ("type", "contacts__city")
    search_fields = ("name", "contacts__city")
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:sales_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = "supplier"

    @admin.display(description="Город")
    def city_filter(self, obj):
        # Проверяем, существует ли contacts и city
        if obj.contacts and obj.contacts.city:
            return obj.contacts.city
        return (
            "-"  # Возвращаем значение по умолчанию, если contacts или city отсутствуют
        )

    @admin.display(description="Уровень")
    def level(self, obj):
        return obj.level

    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=F("debt") - F("debt"))
        self.message_user(request, f"Очищена задолженность для {updated} объектов")

    fieldsets = (
        ("Основная информация", {"fields": ("name", "type", "supplier", "debt")}),
        ("Контакты", {"fields": ("contacts",)}),
        ("Продукты", {"fields": ("products",)}),
    )
    readonly_fields = ("created_at",)
    filter_horizontal = ("products",)
