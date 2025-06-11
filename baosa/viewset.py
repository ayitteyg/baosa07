from rest_framework import viewsets
from .models import Member, Receipt, Payment, Event, Message
from .serializers import *
from .models import Event, AnnualDues
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from collections import defaultdict
from rest_framework import status





class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]  # Add if needed


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptListSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    
class MyEventsViewSet(viewsets.ModelViewSet):
    queryset = MyEvents.objects.all()
    serializer_class = MyEventsSerializer
   

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer



  
    


    
    
    
