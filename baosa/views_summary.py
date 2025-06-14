from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
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
    MyEventsSerializer, EventSerializer, MemberCreateViewSerializer, MemberSummarySerializer
)
from rest_framework.decorators import action
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
        
        
        annual_dues_aggregate = AnnualDues.objects.filter(category='dues').aggregate(total=Sum('amount'))
       #print("🔍 Annual dues aggregate:", annual_dues_aggregate)

        total_annual_dues = int(annual_dues_aggregate['total'] if annual_dues_aggregate['total'] is not None else 0)
        #print("✅ Total annual dues computed:", total_annual_dues)

        # Compute annual dues
        # total_annual_dues = AnnualDues.objects.filter(category='dues').aggregate(
        #     total=Sum('amount')
        # )['total'] or 0
        
       # total_annual_dues = 100.0
       
        difference =  total_dues_paid - (total_annual_dues)
        dues_status = "In advance" if difference >= 0 else "In arrears"
        
        
        #define dues status
        active_threshold = total_annual_dues * 0.7

        # Get the member's receipts
        receipts = Receipt.objects.filter(member=member)
        dues_paid = receipts.filter(category='dues').aggregate(total=Sum('amount'))['total'] or 0
        has_contribution = receipts.filter(category='contribution').exists()
        has_seed_fund = receipts.filter(category='seed_fund').exists()

        is_active = (
            dues_paid >= active_threshold and
            has_contribution and
            has_seed_fund
        )

        result.update({
            'total_annual_dues': float(total_annual_dues),
            'dues_difference': abs(difference),
            'dues_status': dues_status,
            "status": "active" if is_active else "inactive"
        })

       # print("➡️ Final result returned to frontend:", result)

        return Response(result, status=status.HTTP_200_OK)




# class MemberViewSetDashboard(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]  # Add if needed
    

    @action(detail=False, methods=['get'])
    def summary(self, request):
        members = self.get_queryset()
        total_members = members.count()

        
        annual_dues_aggregate = AnnualDues.objects.filter(category='dues').aggregate(total=Sum('amount'))
       #print("🔍 Annual dues aggregate:", annual_dues_aggregate)

        total_expected_dues = int(annual_dues_aggregate['total'] if annual_dues_aggregate['total'] is not None else 0)
        #print("✅ Total annual dues computed:", total_annual_dues)

        active_dues_threshold = int(total_expected_dues) * 0.7

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

        print(summary)
        return Response(summary, status=status.HTTP_200_OK)



class MemberSummaryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        members = Member.objects.all()
        total_members = members.count()

        # Aggregate total expected dues
        annual_dues_aggregate = AnnualDues.objects.filter(category='dues').aggregate(total=Sum('amount'))
        total_expected_dues = int(annual_dues_aggregate['total'] if annual_dues_aggregate['total'] is not None else 0)
        active_dues_threshold = total_expected_dues * 0.7

        # Fetch all receipts
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

        return Response(summary, status=status.HTTP_200_OK)


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
        #print(result)
        return Response(result, status=status.HTTP_200_OK)