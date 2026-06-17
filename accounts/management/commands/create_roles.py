from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        roles = [
            'Super Admin',
            'Branch Manager',
            'Cashier',
            'Accountant',
            'Store Keeper',
            'HR Officer',
            'Pharmacist',
            'Sales Representative'
        ]

        for role in roles:
            Group.objects.get_or_create(name=role)

        self.stdout.write(
            self.style.SUCCESS('Roles created successfully')
        )
