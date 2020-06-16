from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'create super admin user for application'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() < 1:
            username = 'admin'
            password = 'admin'
            email = 'admin@nocompay.com'

            user = User.objects.create_user(username=username, password=password, email=email, is_active=True, is_staff=True, is_superuser=True)
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully creacted "%s" user' % username))
    