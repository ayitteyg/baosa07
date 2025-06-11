import json
from django.core.management.base import BaseCommand
from baosa.models import Receipt, Member  # Adjust this import to your app
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = 'Load process receipts for members'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to load receipts...")

        # Path to your JSON file
        file_path = 'data_json/members_receipt.json'  # Adjust this path
       
        try:
            with open(file_path, 'r') as file:
                receipts_data = json.load(file)

            for receipt in receipts_data:
                member_name = receipt['member']
                try:
                    member = Member.objects.get(name=member_name)
                except Member.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Member '{member_name}' not found. Skipping."))
                    continue

                Receipt.objects.create(
                    member=member,
                    receipt_date=parse_date(receipt['receipt_date']),
                    category=receipt['category'],
                    amount=receipt['amount'],
                    detail=receipt['detail']
                )

                self.stdout.write(self.style.SUCCESS(f"Added receipt for {member_name}."))

            self.stdout.write(self.style.SUCCESS("Bulk receipt loading complete."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found at {file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON file. Check the file format."))
