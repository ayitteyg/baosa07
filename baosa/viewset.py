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
    

    @action(detail=False, methods=['get'])
    def summary(self, request):
        members = self.get_queryset()
        total_members = members.count()

        # Total expected dues
        total_expected_dues = AnnualDues.objects.filter(category='dues').aggregate(
            total=Sum('amount')
        )['total'] or 0

        active_dues_threshold = total_expected_dues * 0.7

        # Fetch all receipts in one query
        receipts = Receipt.objects.select_related('member').all()

        # Organize receipts by member ID and category
        member_receipts = defaultdict(lambda: {'dues': 0, 'contribution': 0, 'seed_fund': 0})

        for r in receipts:
            member_id = r.member_id
            if r.category == 'dues':
                member_receipts[member_id]['dues'] += r.amount
            elif r.category == 'contribution':
                member_receipts[member_id]['contribution'] += r.amount
            elif r.category == 'seed_fund':
                member_receipts[member_id]['seed_fund'] += r.amount

        # Count active members
        total_active = 0
        for member in members:
            rec = member_receipts.get(member.id, {})
            if (
                rec.get('dues', 0) >= active_dues_threshold and
                rec.get('contribution', 0) > 0 and
                rec.get('seed_fund', 0) > 0
            ):
                total_active += 1

        total_inactive = total_members - total_active
        
        summary = {
            'total_members': total_members,
            'total_male': members.filter(gender='M').count(),
            'total_female': members.filter(gender='F').count(),
            'total_married': members.filter(marital_status='Married').count(),
            'total_single': members.filter(marital_status='single').count(),
            'total_active': total_active,
            'total_inactive': total_inactive,
        }

        #print(summary)
        return Response(summary, status=status.HTTP_200_OK)


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



  
    


    
    
    
