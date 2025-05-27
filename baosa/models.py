from django.contrib.auth import get_user_model  # Add this import at the top
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth.models import BaseUserManager


# Create your models here.


class Member(models.Model):
    CATEGORY_CHOICES = [
        ('executive', 'Executive'),
        ('member', 'Member'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member_profile',
        null=True,
        blank=True  # Recommended to add this
    )
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    work = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='member')
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        User = get_user_model()  # Get the actual User model class
        if not self.user_id:  # Only if user isn't already assigned
            try:
                self.user = User.objects.get(username=self.contact)
            except User.DoesNotExist:
                pass  # Or handle the case where user doesn't exist
        super().save(*args, **kwargs)



class Receipt(models.Model):
    CATEGORY_CHOICES = [
        ('dues', 'Dues'),
        ('seed_fund', 'Seed Fund'),
        ('contribution', 'Contribution'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    receipt_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    detail = models.TextField()

    def __str__(self):
        return f"{self.member.name} - {self.category} - {self.amount}"



class AnnualDues(models.Model):
    year = models.CharField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.year} - {self.amount}"



class Payment(models.Model):
    payment_date = models.DateField()
    payment_to = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_details = models.TextField()

    def __str__(self):
        return f"{self.payment_to} - {self.amount}"



class MyEvents(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Event(models.Model):
    event = models.ForeignKey(MyEvents, on_delete=models.CASCADE, default="")
    event_date = models.DateField()
    event_description = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default="")
    def __str__(self):
        return self.event


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.name}"
    

class CustomUser(AbstractUser):
    is_executive = models.BooleanField(default=False)

    def __str__(self):
        return self.username