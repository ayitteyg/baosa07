from django.shortcuts import render, redirect
from django.views import generic, View
from django.views.generic import TemplateView
from .forms import PasswordlessAuthForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from .bulk_data_test import run_data
from . models import Member, AnnualDues, CustomUser, Receipt
from . functions import print_model_objects, reset_model_data, convert_to_json, read_file
from .views_summary import MemberReceiptsView
# Create your views here.


#run_data()

#reset_model_data(AnnualDues)
#print_model_objects(Member)
#convert_to_json('members_receipt')
#read_file('members_data')


class CustomLoginView(View):
    template_name = 'root/login.html'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.redirect_authenticated_user:
            return redirect(self.get_success_url())
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        print(user)

        if user is not None:
            login(request, user)
            return redirect(self.get_success_url())
        else:
            # Optionally pass an error message back to the template
            return render(request, self.template_name, {
                'error': 'Invalid username or password',
                'username': username
            })

    def get_success_url(self):
        return reverse_lazy('homepage')
login_view = CustomLoginView.as_view()





def login_failed_view(request):
    return render(request, 'root/login_fail.html')


def login_out_view(request):
    return render(request, 'root/login.html')

class HomepageView(TemplateView):
    template_name = 'root/homepage.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user)

        if user.is_authenticated:
            context['url'] = reverse("homepage")
        #     if user.is_local:
        #         context['report_url'] = reverse("report_dashboard_local")
        #     elif user.is_district:
        #         context['report_url'] = reverse("report_dashboard_dist")
        #     elif user.is_officer:
        #         context['report_url'] = reverse("report_dashboard_officer")
        #     else:
        #         context['report_url'] = reverse("homepage")
        else:
            context['url'] = reverse("login")

        return context
    
homepage_page_view = HomepageView.as_view() 



from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import Member  # Update with your actual app name



@csrf_exempt
def get_member_id(request):
    if request.method == 'GET':
        username = request.GET.get('username')
    elif request.method == 'POST':
        import json
        body = json.loads(request.body)
        username = body.get('username')
    else:
        return JsonResponse({'error': 'Only GET or POST allowed'}, status=405)

    try:
        User = get_user_model()
        user = User.objects.get(username=username)
        member = user.member_profile
        return JsonResponse({'user_id': member.user})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member profile not found'}, status=404)