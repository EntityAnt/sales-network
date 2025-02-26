from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Contacts(models.Model):
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contact_user",
        verbose_name="Создатель",
        help_text="Укажите создателя контакта",
    )


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="product_user",
        verbose_name="Создатель",
        help_text="Укажите создателя продукта",
    )

    def __str__(self):
        return f"{self.name} {self.model}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class NetworkNode(models.Model):
    FACTORY = 'factory'
    RETAIL = 'retail'
    ENTREPRENEUR = 'entrepreneur'
    NODE_TYPES = (
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    type = models.CharField(
        max_length=20,
        choices=NODE_TYPES,
        verbose_name='Тип звена'
    )
    contacts = models.OneToOneField(
        Contacts,
        on_delete=models.CASCADE,
        verbose_name='Контакты'
    )
    products = models.ManyToManyField(
        Product,
        verbose_name='Продукты'
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Поставщик'
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Задолженность'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="node_user",
        verbose_name="Создатель",
        help_text="Укажите создателя звена сети",
    )

    def clean(self):
        if self.type == NetworkNode.FACTORY:
            if self.supplier is not None:
                raise ValidationError("Завод не может иметь поставщика.")
        else:
            if self.supplier is None:
                raise ValidationError("Незаводское звено должно иметь поставщика.")
            current = self.supplier
            level = 1
            while current.type != NetworkNode.FACTORY:
                current = current.supplier
                level += 1
                if current is None:
                    raise ValidationError("Цепочка поставщиков должна заканчиваться заводом.")
                if level > 2:
                    raise ValidationError("Максимальный уровень иерархии — 2.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def level(self):
        if self.type == NetworkNode.FACTORY:
            return 0
        return self.supplier.level + 1

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
