from rest_framework import viewsets
from .models import Member, Receipt, Payment, Event, Message
from .serializers import *
from .models import Event
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response



class MemberViewSet2(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberListSerializer
    

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        summary = {
            'total_members': queryset.count(),
            'total_male': queryset.filter(gender='M').count(),
            'total_female': queryset.filter(gender='F').count(),
            'total_married': queryset.filter(marital_status='Married').count(),
            'total_single': queryset.filter(marital_status='single').count(),
        }
        serializer = MemberSummarySerializer(summary)
        return Response(serializer.data)

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



  
    


    
    
    
