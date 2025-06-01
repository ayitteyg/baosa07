from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Receipt, Member, AnnualDues, Payment, MyEvents, Event
from datetime import datetime
from random import choice
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ReceiptCreateSerializer, MemberSerializer, 
    PaymentCreateSerializer, PaymentListSerializer,
    MyEventsSerializer, EventSerializer, MemberCreateViewSerializer
)

from collections import defaultdict
from decimal import Decimal
from django.db.models.functions import ExtractYear





class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]


class MemberReceiptsView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        
        member = choice(Member.objects.all())
        
        receipts = Receipt.objects.filter(member=member).order_by('-receipt_date')
        
        # Group by year
        grouped_receipts = {}
        for receipt in receipts:
            year = receipt.receipt_date.year
            if year not in grouped_receipts:
                grouped_receipts[year] = []
            grouped_receipts[year].append(receipt)
        
        serialized_data = []
        for year, year_receipts in grouped_receipts.items():
            serialized_data.append({
                'year': year,
                'receipts': [{
                    'date': r.receipt_date.strftime('%Y-%m-%d'),
                    'category': r.get_category_display(),
                    'amount': float(r.amount),
                    'detail': r.detail
                } for r in year_receipts]
            })
        #print(serialized_data)
        return Response(serialized_data, status=status.HTTP_200_OK)



class ReceiptSummaryView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        
        summary = Receipt.objects.filter(member=member).values('category').annotate(
            total=Sum('amount')
        )
        
        result = {
            'seed_fund': 0,
            'dues': 0,
            'contribution': 0
        }

        for item in summary:
            if item['category'] == 'seed_fund':
                result['seed_fund'] = float(item['total'])
            elif item['category'] == 'dues':
                result['dues'] = float(item['total'])
            elif item['category'] == 'contribution':
                result['contribution'] = float(item['total'])

        # Ensure total dues paid exists
        total_dues_paid = result.get('dues', 0)

        # Compute annual dues
        total_annual_dues = AnnualDues.objects.aggregate(total=Sum('amount'))['total'] or 0

        difference =  total_dues_paid - float(total_annual_dues)
        dues_status = "In advance" if difference >= 0 else "In arrears"

        result.update({
            'total_annual_dues': float(total_annual_dues),
            'dues_difference': abs(difference),
            'dues_status': dues_status
        })

        print("➡️ Final result returned to frontend:", result)

        return Response(result, status=status.HTTP_200_OK)



"""  create/update viewset  """
class ReceiptCreateView(generics.CreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptCreateSerializer
    permission_classes = [IsAuthenticated]



class MyEventsCreateView(generics.CreateAPIView):
    queryset = MyEvents.objects.all()
    serializer_class = MyEventsSerializer
    


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]



class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentListSerializer  
    permission_classes = [IsAuthenticated]




class MemberCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberCreateViewSerializer


class FinanceSummaryView2(APIView):
    def get(self, request):
        bal_bf = Decimal('2000.00')

        # Total receipts by category
        receipt_totals = Receipt.objects.values('category').annotate(total=Sum('amount'))
        category_totals = {
            'dues': Decimal('0.00'),
            'seed_fund': Decimal('0.00'),
            'contribution': Decimal('0.00'),
        }
        for item in receipt_totals:
            category = item['category']
            if category in category_totals:
                category_totals[category] = item['total'] or Decimal('0.00')

        total_receipts = bal_bf + sum(category_totals.values())

        # Yearly receipts breakdown
        yearly_receipts_qs = Receipt.objects.annotate(year=ExtractYear('receipt_date')) \
            .values('category', 'year') \
            .annotate(total=Sum('amount'))

        yearly_receipts = defaultdict(lambda: {})
        for item in yearly_receipts_qs:
            yearly_receipts[item['category']][item['year']] = float(item['total'])

        # Total payments
        total_payments = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Yearly payments breakdown (with member name)
        payments_qs = Payment.objects.annotate(year=ExtractYear('payment_date')) \
            .values('year', 'payment_to__name') \
            .annotate(total=Sum('amount'))

        yearly_payments = defaultdict(list)
        for item in payments_qs:
            yearly_payments[item['year']].append({
                'payment_to': item['payment_to__name'],
                'amount': float(item['total']),
            })

        current_balance = total_receipts - total_payments

        return Response({
            'total_receipts': float(total_receipts),
            'components': {
                'bal_bf': float(bal_bf),
                'dues': float(category_totals['dues']),
                'seed_fund': float(category_totals['seed_fund']),
                'contribution': float(category_totals['contribution']),
            },
            'yearly_receipts': yearly_receipts,
            'total_payments': float(total_payments),
            'yearly_payments': yearly_payments,
            'current_balance': float(current_balance),
        }, status=status.HTTP_200_OK)



class FinanceSummaryView(APIView):
    def get(self, request):
        bal_bf = 2000  # Static balance brought forward

        # Aggregate receipts
        total_receipts = Receipt.objects.values('category').annotate(total=Sum('amount'))

        summary = {
            'bal_bf': bal_bf,
            'total_dues': 0,
            'total_seed_fund': 0,
            'total_contribution': 0
        }

        for item in total_receipts:
            if item['category'] == 'dues':
                summary['total_dues'] = float(item['total'])
            elif item['category'] == 'seed_fund':
                summary['total_seed_fund'] = float(item['total'])
            elif item['category'] == 'contribution':
                summary['total_contribution'] = float(item['total'])

        summary['total_receipts'] = (
            bal_bf + summary['total_dues'] +
            summary['total_seed_fund'] + summary['total_contribution']
        )

        # Yearly breakdown
        yearly_receipts = Receipt.objects.annotate(year=ExtractYear('receipt_date')).values('year', 'category').annotate(total=Sum('amount'))

        # Aggregate payments
        total_payments = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_payments = float(total_payments)

        payments_details = list(Payment.objects.annotate(
            year=ExtractYear('payment_date')
        ).values('year', 'payment_to__name', 'amount'))

        current_balance = summary['total_receipts'] - total_payments

        result = {
            'summary': summary,
            'yearly_receipts': yearly_receipts,
            'total_payments': total_payments,
            'payments_details': payments_details,
            'current_balance': current_balance
        }
        print(result)
        return Response(result, status=status.HTTP_200_OK)