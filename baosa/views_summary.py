from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Receipt, Member, AnnualDues, Payment
from datetime import datetime
from random import choice
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ReceiptCreateSerializer, MemberSerializer, PaymentCreateSerializer, PaymentListSerializer
)



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



class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]



class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentListSerializer  
    permission_classes = [IsAuthenticated]


