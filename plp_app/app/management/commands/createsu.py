from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        try:
            user_search= User.objects.get(username="admin")
        
        except:
            user = User(
                username="admin",
                email="admin@admin.com",
                first_name="main",
                last_name="admin",
            )
            user.set_password("admin")
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print("Superuser created.")
