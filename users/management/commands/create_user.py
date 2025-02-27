from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "user1@example.com"
        password = "1234"
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = False
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Создан пользователь\nemail для входа: {email}\nпароль: {password}"
            )
        )
