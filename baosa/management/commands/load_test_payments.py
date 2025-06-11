from django.core.management.base import BaseCommand
from django.utils import timezone
from baosa.models import Payment, Member  # Replace 'yourapp' with your actual app name
import random
from random import choice, randint, uniform
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Loads test payment data for specified contacts'

    def handle(self, *args, **options):
        contacts = [
            '0245416427',
            '0277343287',
            '0556809020',
            '0249438545',
            '0598446338'

        ]
        
        # Amounts to choose from randomly
        amounts = [1150.00, 1520.00, 890.00, 1250.00, 1600.00]
        
        # Payment details options
        details_options = [
            "support for funeral",
            "Marriage support",
            "support for hospitalization",
            "Donation"
        ]
        
        created_count = 0
        start_date = datetime(2024, 9, 1)
        end_date = datetime(2025, 12, 31)
        date_range_days = (end_date - start_date).days
        
        for contact in contacts:
            try:
                # Find member by contact number
                member = Member.objects.get(contact=contact)
                
                # Create 1-3 random payments for each member
                for _ in range(random.randint(1,1)):
                    payment = Payment(
                        payment_date=make_aware(start_date + timedelta(days=randint(0, date_range_days))),
                        payment_to=member,
                        amount=random.choice(amounts),
                        payment_details=random.choice(details_options)
                    )
                    payment.save()
                    created_count += 1
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'Created payment: {member} - {payment.amount}'
                    ))
                
            except Member.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Member with contact {contact} not found, skipping...'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} test payments'
        ))