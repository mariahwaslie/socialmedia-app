from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create fake users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker()

        for _ in range(total):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='password',  # you can customize or randomize this
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))

if __name__ == '__main__':
    Command().run()
