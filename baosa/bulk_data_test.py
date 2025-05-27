from .models import Member, Receipt, AnnualDues, CustomUser, MyEvents
from random import choice, uniform
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from faker import Faker
from random import choice
from random import choice, randint, uniform
from django.contrib.auth import get_user_model
from django.db import IntegrityError  # Import IntegrityError




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



def create_single_member(name, contact, location, work, marital_status, category='member'):
    User = get_user_model()

    # Create or get user
    user, created = User.objects.get_or_create(
        username=contact,
        defaults={'is_executive': category == 'executive'}
    )
    if created:
        user.set_password('baosa@2007')  # Default password
        user.save()

    # Create Member
    member, created = Member.objects.get_or_create(
        contact=contact,
        defaults={
            'user': user,
            'name': name,
            'location': location,
            'work': work,
            'marital_status': marital_status,
            'category': category
        }
    )

    print(f"✅ Member {'created' if created else 'already exists'}: {member.name}")
    return member

    
    
    
def bulk_create_members(members_data: list):
    created_members = []

    for data in members_data:
        name = data.get('name')
        contact = data.get('contact')
        location = data.get('location')
        work = data.get('work')
        marital_status = data.get('marital_status')
        category = data.get('category', 'member')

        member = create_single_member(
            name=name,
            contact=contact,
            location=location,
            work=work,
            marital_status=marital_status,
            category=category
        )
        created_members.append(member)

    print(f"✅ Bulk created {len(created_members)} members.")
    return created_members



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
    try:
        # Create single user
        user = CustomUser.objects.create_user(
            username='1234567890',  # Should match member's contact if using your association logic
            password='baosa@2007',
        )
        print(f"✅ Successfully created user: {user.username}")
        return [user]  # Return as list to match your original return format
    
    except IntegrityError:
        print("⚠️ User already exists")
        return []
    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")
        return []



def create_app_users(usernames: list):
    CustomUser = get_user_model()
    count = 0

    for usr in usernames:
        if not CustomUser.objects.filter(username=usr).exists():
            user = CustomUser(username=usr)
            user.set_password('baosa@2007')  # ✅ hashes password
            user.save()
            count += 1

    print(f"✅ Successfully created {count} users.")



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