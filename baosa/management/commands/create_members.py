from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from baosa.models import Member  # Replace with your actual app name
from django.db import transaction
import json


    

class Command(BaseCommand):
    help = 'Bulk create users and members'

    def handle(self, *args, **kwargs):
        try:
            with open('data_json/members_data.json', 'r') as f:
                members_list = json.load(f)
            self.bulk_create_members(members_list)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("❌ File not found: data_json/members_data.json"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("❌ Invalid JSON format."))
    
    
    
    def bulk_create_members(self, members_list):
       
        User = get_user_model()
        new_users = []
        new_members = []

        # Fetch existing usernames from the database
        existing_usernames = set(User.objects.filter(
            username__in=[m['contact'] for m in members_list]
        ).values_list('username', flat=True))

        # Fetch usernames of users who already have members
        existing_member_usernames = set(Member.objects.filter(
            user__username__in=[m['contact'] for m in members_list]
        ).values_list('user__username', flat=True))

        # Keep track of contacts already processed to avoid duplicates in input
        processed_contacts = set(existing_usernames)

        with transaction.atomic():
            # First pass: create new users
            for data in members_list:
                contact = data['contact']
                if contact in processed_contacts:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ User {contact} already exists or is duplicated. Skipping user creation."))
                    continue

                user = User(username=contact)
                user.set_password('baosa@2007')
                new_users.append(user)
                processed_contacts.add(contact)

            created_users = User.objects.bulk_create(new_users)

            # Build a mapping of all users (new and existing)
            user_map = {u.username: u for u in User.objects.filter(
                username__in=[m['contact'] for m in members_list]
            )}

            # Second pass: create members only for users without existing members
            for data in members_list:
                contact = data['contact']

                if contact not in user_map:
                    continue  # Shouldn't happen, but safe

                if contact in existing_member_usernames:
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ Member for user {contact} already exists. Skipping member creation."))
                    continue

                member = Member(
                    user=user_map[contact],
                    name=data['name'],
                    gender=data['gender'],
                    contact=contact,
                    location=data['location'],
                    work=data['work'],
                    marital_status=data['marital_status'],
                    next_of_kin=data['next_of_kin'],
                    next_of_kin_cont=data['next_of_kin_cont'],
                    category=data.get('category', 'member')
                )
                new_members.append(member)

            if new_members:
                Member.objects.bulk_create(new_members)

            self.stdout.write(self.style.SUCCESS(
                f"✅ Successfully created {len(new_users)} users and {len(new_members)} members."))


    # def bulk_create_members(self, members_list):
    #     User = get_user_model()
    #     new_users = []
    #     new_members = []

    #     # Fetch existing usernames from the database
    #     existing_usernames = set(User.objects.filter(
    #         username__in=[m['contact'] for m in members_list]
    #     ).values_list('username', flat=True))

    #     # Keep track of contacts already processed to avoid duplicates in input
    #     processed_contacts = set(existing_usernames)

    #     with transaction.atomic():
    #         # First pass: create users
    #         for data in members_list:
    #             contact = data['contact']
    #             if contact in processed_contacts:
    #                 self.stdout.write(self.style.WARNING(
    #                     f"⚠️ User {contact} already exists or is duplicated. Skipping."))
    #                 continue

    #             user = User(username=contact)
    #             user.set_password('baosa@2007')
    #             new_users.append(user)
    #             processed_contacts.add(contact)

    #         created_users = User.objects.bulk_create(new_users)

    #         # Map all relevant users (both new and existing) by username
    #         user_map = {u.username: u for u in User.objects.filter(
    #             username__in=[m['contact'] for m in members_list]
    #         )}

    #         # Fetch usernames of users who already have members
    #         existing_member_usernames = set(Member.objects.filter(
    #             user__username__in=[m['contact'] for m in members_list]
    #         ).values_list('user__username', flat=True))

    #         # Second pass: create members
    #         for data in members_list:
    #             contact = data['contact']
    #             if contact not in user_map:
    #                 continue  # This should rarely happen but is a safe check

    #             if contact in existing_member_usernames:
    #                 self.stdout.write(self.style.WARNING(
    #                     f"⚠️ Member for user {contact} already exists. Skipping."))
    #                 continue

    #             member = Member(
    #                 user=user_map[contact],
    #                 name=data['name'],
    #                 gender=data['gender'],
    #                 contact=contact,
    #                 location=data['location'],
    #                 work=data['work'],
    #                 marital_status=data['marital_status'],
    #                 next_of_kin=data['next_of_kin'],
    #                 next_of_kin_cont=data['next_of_kin_cont'],
    #                 category=data.get('category', 'member')
    #             )
    #             new_members.append(member)

    #         Member.objects.bulk_create(new_members)

    #         self.stdout.write(self.style.SUCCESS(
    #             f"✅ Successfully created {len(new_users)} users and {len(new_members)} members."))
