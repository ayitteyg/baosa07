from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from baosa.models import Member  # Replace with your actual app name
from django.db import transaction

class Command(BaseCommand):
    help = 'Bulk create users and members'

    def handle(self, *args, **kwargs):
        members_list = [
            {
                'name': 'John Doe',
                'contact': '0551234567',
                'location': 'Accra',
                'work': 'Carpenter',
                'marital_status': 'single',
                'category': 'member'
            },
            {
                'name': 'Jane Smith',
                'contact': '0249876543',
                'location': 'Kumasi',
                'work': 'Trader',
                'marital_status': 'married',
                'category': 'executive'
            }
        ]

        self.bulk_create_members(members_list)

    def bulk_create_members(self, members_list):
        User = get_user_model()
        new_users = []
        new_members = []

        existing_usernames = set(User.objects.filter(
            username__in=[m['contact'] for m in members_list]
        ).values_list('username', flat=True))

        with transaction.atomic():
            for data in members_list:
                contact = data['contact']
                if contact in existing_usernames:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ User {contact} already exists. Skipping."))
                    continue

                user = User(username=contact)
                user.set_password('baosa@2007')
                new_users.append(user)

            created_users = User.objects.bulk_create(new_users)

            user_map = {u.username: u for u in User.objects.filter(
                username__in=[m['contact'] for m in members_list]
            )}

            for data in members_list:
                contact = data['contact']
                if contact not in user_map:
                    continue

                member = Member(
                    user=user_map[contact],
                    name=data['name'],
                    contact=contact,
                    location=data['location'],
                    work=data['work'],
                    marital_status=data['marital_status'],
                    category=data.get('category', 'member')
                )
                new_members.append(member)

            Member.objects.bulk_create(new_members)
            self.stdout.write(self.style.SUCCESS(
                f"✅ Created {len(new_members)} members and users."))
