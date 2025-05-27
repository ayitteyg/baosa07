from rest_framework import serializers
from .models import Member, Receipt, Payment, Event, Message, MyEvents



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('date_joined',)


class MemberSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name']


class MemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('date_joined',)
        

class MemberSummarySerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    total_male = serializers.IntegerField()
    total_female = serializers.IntegerField()
    total_married = serializers.IntegerField()
    total_single = serializers.IntegerField()

class ReceiptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        

# For writes (create/update)
class ReceiptCreateSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)  # For displaying member details
    class Meta:
        model = Receipt
        fields = ['member', 'receipt_date', 'category', 'amount', 'detail']
        extra_kwargs = {
            'receipt_date': {'required': True},
            'category': {'required': True},
            'amount': {'required': True}
        }
        


class PaymentCreateSerializer(serializers.ModelSerializer):
    payment_to = MemberSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['payment_to', 'payment_date', 'amount', 'payment_details']
        extra_kwargs = {
            'payment_date': {'required': True},
            'amount': {'required': True, 'min_value': 0.01}
        }


class MyEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyEvents
        fields = ['id', 'name']



class EventSerializer(serializers.ModelSerializer):
    event = MyEventsSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=MyEvents.objects.all(),
        source='event',
        write_only=True
    )
    member = MemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        source='member',
        write_only=True
    )
    
    class Meta:
        model = Event
        fields = [
            'id', 'event', 'event_id', 
            'event_date', 'event_description',
            'member', 'member_id'
        ]
        extra_kwargs = {
            'event_date': {'required': True},
            'event_description': {'required': True}
        }