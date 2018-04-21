from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
import datetime, time
from django.views.generic import View


	# search subject
	# get method로 요청이 들어오면 사용자 로그인 체크
	# URL query: q, hundreds, department, category, start_time, end_time, credit
	# start_time, end_time = 'WED 15:00'
	# 검색 조건에 따라 해당 값이 쿼리에 없을 수도 있음
	# ex) copy_timetable/?q=윤은영&hundreds=1
	# 검색 조건에 맞는 subject들을 학수번호로 정렬하여 JSON으로 return

	#searched_subject = list of {'subejct':subject, 'period':list of periods}




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
	subjects = Subject.objects.all()

	if request.GET.get('q') :
		subjects = subjects.filter(Q(professor__contains = q) | Q(name__contains = q) || Q(code__contains = q))
		aliases = Alias.objects.filter(nickname__contains = q)
		subjects = list(set(subjects + [alias.original for alias in aliases]))

	hundreds = []
	if request.GET.get('1hundred') :
		credits.append(1)
	if request.GET.get('2hundred') :
		credits.append(2)
	if request.GET.get('3hundred') :
		credits.append(3)
	if request.GET.get('4hundred') :
		credits.append(4)
	
	if credits :
		subjects.filter(return_hundred in hundreds)

	if request.GET.get('department') :
		subjects = subjects.filter(department__name__contains = q)

	if request.GET.get('category') :
		subjects = subjects.filter(category__category__contains = q)

	if request.GET.get('start_time') :
		start_time = request.GET.get('start_time')
		dayoftheweek = stime[:3]
		stime = datetime.datetime.strptime(stime[4:], "%H:%M").time()
		etime = datetime.datetime.strptime(request.GET.get('end_time')[4:], "%H:%M").time()
		if dayoftheweek == 'MON'
			periods = Period.objects.filter(mon=True)
		elif dayoftheweek == 'TUE'
			periods = Period.object.filter(tue=True)
		elif dayoftheweek == 'WED'
			periods = Period.object.filter(wed=True)
		elif dayoftheweek == 'THR'
			periods = Period.object.filter(thr=True)
		elif dayoftheweek == 'FRI'
			periods = Period.object.filter(fri=True)
		periods = periods.filter(Q(start__gte=stime)&Q(end__lte=etime))
		subjects = list(set(subjects).intersection([period.subject for period in periods]))

	credits = []
	if request.GET.get('1credit') :
		credits.append(1)
	if request.GET.get('2credit') :
		credits.append(2)
	if request.GET.get('3credit') :
		credits.append(3)
	if request.GET.get('4credit') :
		credits.append(4)
	
	if credits :
		subjects.filter(return_credit in credits)


	subjects.order_by('code')

#	for subject in subjects:
#		subject.period_set.all()

	return JsonResponse({'subjects : subjects'})

def add_subject_to_timetable(request):
	return HttpResponse("add_subject_to_timetable")

def delete_subject_to_timetable(request):
	return HttpResponse("delete_subject_to_timetable")
