from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'core/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('core/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'core/checkemail.html')
        else:
            return render(request, 'core/signup.html', {'form': form})

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, 'core/auth_complete.html')
        else:
            return render(request, 'core/auth_failed.html')

@login_required
def timetable(request):
	return HttpResponse("timetable")

@login_required
def select_semester(request):
	return HttpResponse("select_semester")

@login_required
def add_timetable(request):
	return HttpResponse("add_timetable")

@login_required
def delete_timetable(request):
	return HttpResponse("delete_timetable")

@login_required
def copy_timetable(request):
	return HttpResponse("copy_timetable")

@login_required
def search_subject(request):
	return HttpResponse("search_subject")

@login_required
def add_subject_to_timetable(request):
	return HttpResponse("add_subject_to_timetable")

@login_required
def delete_subject_to_timetable(request):
	return HttpResponse("delete_subject_to_timetable")