from django.shortcuts import render
from django.views.generic import View

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

def timetable(request):
	return HttpResponse("timetable")

def select_semester(request):
	return HttpResponse("select_semester")

def add_timetable(request):
	return HttpResponse("add_timetable")

def delete_timetable(request):
	return HttpResponse("delete_timetable")

def copy_timetable(request):
	return HttpResponse("copy_timetable")

def search_subject(request):
	return HttpResponse("search_subject")

def add_subject_to_timetable(request):
	return HttpResponse("add_subject_to_timetable")

def delete_subject_to_timetable(request):
	return HttpResponse("delete_subject_to_timetable")