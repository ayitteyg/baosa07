from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from baosa import viewset
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from .views_summary import (MemberReceiptsView, ReceiptSummaryView, 
                            ReceiptCreateView, MemberListView,
                            PaymentCreateView, PaymentListView)
from .views_rest_framework import CustomAuthToken

from .viewset import (PaymentViewSet, ReceiptViewSet,
                      EventViewSet, MyEventsViewSet, 
                      MemberViewSet2, MemberViewSet)



from .views import (
    login_view,  login_failed_view, homepage_page_view, login_out_view)

router = routers.DefaultRouter()
router.register(r'members', viewset.MemberViewSet)
router.register(r'receipts', viewset.ReceiptViewSet)
router.register(r'payments', viewset.PaymentViewSet)
router.register(r'events', viewset.EventViewSet)
router.register(r'messages', viewset.MessageViewSet)
# router.register(r'members', MemberViewSet2, basename='member')

urlpatterns = [
    path('api/token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('admin_redirect/', lambda request: redirect('/admin/'), name='admin_redirect'),
    path('api/', include(router.urls)),
    path('', login_view, name='login'),
    path('login-failed/', login_failed_view, name='login_failed'),
    path('homepage', homepage_page_view, name='homepage'),
    path('login/', login_out_view, name='logout'),
    
]

urlpatterns += [
    path('api/receipts/member/<int:member_id>/', MemberReceiptsView.as_view()),
    path('api/receipts/summary/<int:member_id>/', ReceiptSummaryView.as_view()),
    path('api/receipts/', ReceiptCreateView.as_view(), name='receipt-create'),
    
    # Receipts
    # path('api/receipts/', ReceiptCreateView.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # }), name='receipt-list'),
    # path('api/receipts/summary/', ReceiptSummaryView.as_view(), name='receipt-summary'),
    # path('api/receipts/member/', MemberReceiptsView.as_view(), name='member-receipts'),  
  ]


  
   
# Payments
urlpatterns +=[
  
    path('api/payments/', PaymentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='payment-list'),
]


#events url
urlpatterns +=[
      
    path('api/events/', EventViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='event-list-create'),
    
    
    path('api/event-types/', MyEventsViewSet.as_view({
    'get': 'list'
    }), name='event-types-list'),
]


#members url
urlpatterns +=[
     path('api/members/', MemberViewSet2.as_view({
        'get': 'list',
        'post': 'create'
    }), name='member-list'),
    path('api/members/summary/', MemberViewSet2.as_view({
        'get': 'summary'
    }), name='member-summary'),
    path('api/members/<int:pk>/', MemberViewSet2.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='member-detail'),
    
    
      # Members
    # path('api/members/', MemberListView.as_view(), name='member-list'),
]