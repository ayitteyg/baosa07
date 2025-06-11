import json
from decimal import Decimal
from random import choice, randint, uniform
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from faker import Faker

from baosa.models import Member, Receipt  # Replace appname with your app

fake = Faker()



# class Command(BaseCommand):
#     help = 'Load dummy receipts for members'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Starting to add dummy receipts...")

#         members = [
#                     "0245848777",
#                     "0555633908",
#                     "245809980",
#                     "0246721982",
#                     "0245690609",
#                     "0248311842",
#                     "0249755457",
#                     "0208636107",
#                     "0543233027",
#                     "0245416427",
#                     "0244926080",
#                     "03142616852",
#                     "0544277039",
#                     "0242165224",
#                     "0277343287",
#                     "0247172317",
#                     "0033755208390",
#                     "0245832652",
#                     "0549053295",
#                     "0249438545",
#                     "0598446338",
#                     "0240807977",
#                     "0240733519",
#                     "0244194945",
#                     "0246191391",
#                     "0268482552",
#                     "0247879897",
#                     "0556809020",
#                     "0245772538",
#                     "0242079382",
#                     "0249604087",
#                     "0240712498",
#                     "0249138467",
#                     "0245863188",
#                     "0240386725",
#                     "0248745349"
#                 ]
      
      
      
#         if not members:
#             self.stdout.write(self.style.ERROR("❌ No members found. Cannot create receipts."))
#             return

#         receipts = []

#         start_date = datetime(2024, 9, 1)
#         end_date = datetime(2025, 12, 31)
#         date_range_days = (end_date - start_date).days

#         for member in members:
#             # Dues: 5-15 fixed amount 20.00
#             dues_count = randint(5, 15)
#             for _ in range(dues_count):
#                 receipt_date = start_date + timedelta(days=randint(0, date_range_days))
#                 receipt_date = make_aware(receipt_date)
#                 receipts.append(
#                     Receipt(
#                         member=member,
#                         receipt_date=receipt_date,
#                         category='dues',
#                         amount=Decimal('20.00'),
#                         detail=fake.sentence(nb_words=10),
#                     )
#                 )

#             # Seed fund: 0 or 1, amount choice from list
#             if randint(0, 1) == 1:
#                 receipt_date = start_date + timedelta(days=randint(0, date_range_days))
#                 receipt_date = make_aware(receipt_date)
#                 receipts.append(
#                     Receipt(
#                         member=member,
#                         receipt_date=receipt_date,
#                         category='seed_fund',
#                         amount=Decimal(str(choice([40, 45, 50]))),
#                         detail=fake.sentence(nb_words=10),
#                     )
#                 )

#             # Contribution: 1-4, amount random 50.00-120.00
#             contribution_count = randint(1, 4)
#             for _ in range(contribution_count):
#                 receipt_date = start_date + timedelta(days=randint(0, date_range_days))
#                 receipt_date = make_aware(receipt_date)
#                 amount = Decimal(f"{uniform(50, 120):.2f}")
#                 receipts.append(
#                     Receipt(
#                         member=member,
#                         receipt_date=receipt_date,
#                         category='contribution',
#                         amount=amount,
#                         detail=fake.sentence(nb_words=10),
#                     )
#                 )

#         Receipt.objects.bulk_create(receipts)

#         self.stdout.write(self.style.SUCCESS(f"✅ Successfully added {len(receipts)} receipt records."))



class Command(BaseCommand):
    help = 'Load dummy receipts for members'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to add dummy receipts...")

        # Phone numbers to process
        member_phones = [
                    "0245848777",
                    "0555633908",
                    "245809980",
                    "0246721982",
                    "0245690609",
                    "0248311842",
                    "0249755457",
                    "0208636107",
                    "0543233027",
                    "0245416427",
                    "0244926080",
                    "03142616852",
                    "0544277039",
                    "0242165224",
                    "0277343287",
                    "0247172317",
                    "0033755208390",
                    "0245832652",
                    "0549053295",
                    "0249438545",
                    "0598446338",
                    "0240807977",
                    "0240733519",
                    "0244194945",
                    "0246191391",
                    "0268482552",
                    "0247879897",
                    "0556809020",
                    "0245772538",
                    "0242079382",
                    "0249604087",
                    "0240712498",
                    "0249138467",
                    "0245863188",
                    "0240386725",
                    "0248745349"
                ]
      
        if not member_phones:
            self.stdout.write(self.style.ERROR("❌ No members found. Cannot create receipts."))
            return

        receipts = []
        start_date = datetime(2024, 9, 1)
        end_date = datetime(2025, 12, 31)
        date_range_days = (end_date - start_date).days

        for phone in member_phones:
            try:
                # Get the Member instance for this phone number
                member = Member.objects.get(contact=phone)
                
                # Dues receipts
                for _ in range(randint(5, 15)):
                    receipts.append(
                        Receipt(
                            member=member,  # Pass the Member instance
                            receipt_date=make_aware(start_date + timedelta(days=randint(0, date_range_days))),
                            category='dues',
                            amount=Decimal('20.00'),
                            detail='dues received'
                        )
                    )

                # Seed fund (50% chance)
                if randint(0, 1) == 1:
                    receipts.append(
                        Receipt(
                            member=member,
                            receipt_date=make_aware(start_date + timedelta(days=randint(0, date_range_days))),
                            category='seed_fund',
                            amount=Decimal(str(choice([40, 45, 50]))),
                            detail='seed fund received'
                        )
                    )

                # Contributions
                for _ in range(randint(1, 4)):
                    receipts.append(
                        Receipt(
                            member=member,
                            receipt_date=make_aware(start_date + timedelta(days=randint(0, date_range_days))),
                            category='contribution',
                            amount=Decimal(f"{uniform(50, 70):.2f}"),
                            detail='contribution received'
                        )
                    )

            except Member.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Member with phone {phone} not found. Skipping."))

        # Bulk create all valid receipts
        Receipt.objects.bulk_create(receipts)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully added {len(receipts)} receipt records."))