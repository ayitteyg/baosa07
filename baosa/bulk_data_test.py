from .models import Member, Receipt, AnnualDues, CustomUser, MyEvents
from random import choice, uniform
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from faker import Faker
from random import choice
from random import choice, randint, uniform
from django.contrib.auth import get_user_model




fake = Faker()



def add_annual_dues():
    dues = [
        AnnualDues(year="2024", amount=Decimal('60.00')),
        AnnualDues(year="2025", amount=Decimal('120.00')),
    ]
    AnnualDues.objects.bulk_create(dues)
    print(f"✅ Successfully added {len(dues)} annual dues.")
    


def load_dummy_members(num_records=50):
    CATEGORY_CHOICES = ['executive', 'member']
    MARITAL_STATUSES = ['married', 'not_married']

    members = []

    for _ in range(num_records):
        member = Member(
            name=fake.name(),
            contact=fake.phone_number(),
            location=fake.city(),
            work=fake.job(),
            marital_status=choice(MARITAL_STATUSES),
            category=choice(CATEGORY_CHOICES),
        )
        members.append(member)

    Member.objects.bulk_create(members)
    print(f"✅ Successfully created {len(members)} dummy members.")



def add_member():
    CATEGORY_CHOICES = ['executive', 'member']
    MARITAL_STATUSES = ['married', 'single']

    members = []

    
    member = Member(
        name=fake.name(),
        contact=fake.phone_number(),
        location=fake.city(),
        work=fake.job(),
        marital_status=choice(MARITAL_STATUSES),
        category=choice(CATEGORY_CHOICES),
        user= CustomUser.objects.get(id=1)
    )
    members.append(member)

    Member.objects.bulk_create(members)
    print(f"✅ Successfully created {len(members)} dummy members.")
    
    



def add_event():
    EVENTS_CHOICES = ['Marraige', 'Funeral', 'Hospitalization']
    myevents = []
    for i in EVENTS_CHOICES:
        events = MyEvents(
            name=i,         
        )
        myevents.append(events)
    MyEvents.objects.bulk_create(myevents)
    print(f"✅ Successfully created {len(myevents)} events.")




def load_bulk_receipts(num_records=50):
    members = Member.objects.all()
    categories = ['dues', 'seed_fund', 'contribution']
    receipts = []

    if not members.exists():
        print("❌ No members found. Cannot create receipts.")
        return

    for _ in range(num_records):
        receipt = Receipt(
            member=choice(members),
            receipt_date=fake.date_between(start_date='-2y', end_date='today'),
            category=choice(categories),
            amount=round(Decimal(uniform(10, 1000)), 2),
            detail=fake.sentence(nb_words=10),
        )
        receipts.append(receipt)

    Receipt.objects.bulk_create(receipts)
    print(f"✅ Successfully created {len(receipts)} receipt records.")
    



def add_receipt():
    members = Member.objects.all()
    categories = ['dues', 'seed_fund', 'contribution']
    receipts = []

    if not members.exists():
        print("❌ No members found. Cannot create receipts.")
        return


    receipt = Receipt(
        member=choice(members),
        receipt_date=fake.date_between(start_date='-2y', end_date='today'),
        category='dues',
        amount=round(Decimal(uniform(10, 1000)), 2),
        detail=fake.sentence(nb_words=10),
    )
    receipts.append(receipt)

    Receipt.objects.bulk_create(receipts)
    print(f"✅ Successfully add {len(receipts)} receipt records.")
    


def create_test_users():
    CustomUser = get_user_model()
    fake = Faker()
    
   
    
    # Create users
    users = []
      
    # Regular users
    # for i in range (1,4):
    #     user = AppUser.objects.create_user(
    #         username=f'user{i}',
    #         email=fake.email(),
    #         password=f'user{i}123',
    #         name=fake.name(),
    #         church=choice([ch[0] for ch in CHURCH]),
    #         department=choice([dpt[0] for dpt in DEPARTMENT_CHOICES]),
    #         contact=f'0244{fake.random_number(digits=6, fix_len=True)}',
    #         is_local=fake.boolean(chance_of_getting_true=70),
    #         is_district=fake.boolean(chance_of_getting_true=30),
    #         is_officer=fake.boolean(chance_of_getting_true=20)
    #     )
    #     users.append(user)
        
    
    user = CustomUser.objects.create_user(
            username='Akwasi Owusu',
            email=fake.email(),
            password='owusu123',
            name=fake.name(),
            church='Achimota',
            department="Interest Coordinator",
            contact=f'0244{fake.random_number(digits=6, fix_len=True)}',
            is_local=True,
            is_district=False,
            is_officer=False
        )
    
    users.append(user)
        
    print(f"✅ Successfully created {len(users)} users data.")
    return users


#runing data
def run_data():
    #load_bulk_receipts()
    #load_dummy_members()
    #add_annual_dues()
    #add_member()
    #add_receipt()
    #add_event()
   
    #create_test_users()
    pass