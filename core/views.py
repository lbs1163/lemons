from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

from .models import *
from .forms import SignupForm
from .tokens import account_activation_token

import datetime, time
import json

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
    semesters = Semester.objects.all()
    departments = Department.objects.all()
    categories = Category.objects.all()
    return render(request, "core/test.html", {'semesters': semesters, 'departments': departments, 'categories': categories})

@login_required
def select_semester(request):
    if request.POST.get(semester) == None:
        raise Http404()
    dump = Timetable.objects.filter(semester = request.POST.get(semester))
    return JsonResponse(dump)

@login_required
def add_timetable(request):
    if request.POST.get(semester) == None:
        raise Http404()
    dump = json.dumps(Timetable.objects.create(user = request.user, semester = request.POST.get(semester)))
    return JsonResponse(dump)

@login_required
def delete_timetable(request, pk):
    del_table = get_object_or_404(Timetable, pk = pk)
    if del_table.user == request.user:
        delete(del_table)
        return JsonResponse("성공적으로 삭제했습니다.", safe = False)
    else:
        return JsonResponse("다른 유저의 시간표입니다. 삭제하지 못했습니다", safe = False)

@login_required
def copy_timetable(request, pk):
    table = get_object_or_404(Timetable, pk = pk)
    if table.user == request.user:
        cpy_table = Timetable.objects.create(user = request.user, semester = request.POST.get(semester))
        cpy_table.subjects = table.subjects
        return JsonResponse(json.dumps(cpy_table))
    return JsonResponse("다른 유저의 시간표입니다. 복사하지 못했습니다.", safe = False)

@login_required
def search_subject(request):
	subjects = Subject.objects.all()

	check = "lets check "
	print(check)

	if request.GET.get('q') :
		q = request.GET.get('q')
		aliases = Alias.objects.filter(nickname__contains = q)
		aliaspks = [alias.original.pk for alias in aliases] 

		print(q)
		subjects = subjects.filter(Q(professor__contains = q) | Q(name__contains = q) | Q(code__contains = q) | Q(pk__in = aliaspks))
		
		check+="q "

	hundreds = ""
	if request.GET.get('1hundred') :
		hundreds+="1"
	if request.GET.get('2hundred') :
		hundreds+="2"
	if request.GET.get('3hundred') :
		hundreds+="3"
	if request.GET.get('4hundred') :
		hundreds+="4"
	
	if hundreds :
		hundredregex = r'^[A-Z]+[' + hundreds + r'][0-9A-Za-z]*$'
		subjects.filter(code = hundredregex)
		check += "hundreds "

	if request.GET.get('department') :

		subjects = subjects.filter(department__name__contains = request.GET.get('department'))
		check += "department "

	if request.GET.get('category') :
		subjects = subjects.filter(category__category__contains = request.GET.get('category'))
		check += "category "

	if request.GET.get('start_time') :
		start_time = request.GET.get('start_time')
		dayoftheweek = start_time[:3]
		stime = datetime.datetime.strptime(start_time[4:], "%H:%M").time()
		end_time = request.GET.get('end_time')
		etime = datetime.datetime.strptime(end_time[4:], "%H:%M").time()
		print(stime)
		print(etime)
		if dayoftheweek == "MON" :
			periods = Period.objects.filter(mon=True)
		elif dayoftheweek == "TUE" :
			periods = Period.object.filter(tue=True)
		elif dayoftheweek == "WED" :
			periods = Period.object.filter(wed=True)
		elif dayoftheweek == "THR" :
			periods = Period.object.filter(thr=True)
		elif dayoftheweek == "FRI" :
			periods = Period.object.filter(fri=True)
		periods = periods.filter(Q(start__gte=stime)&Q(end__lte=etime))
		periodsubjectpks = [period.subject.pk for period in periods]
		subjects = subjects.filter(pk__in = periodsubjectpks)
		check += "time "

	credits = ""
	if request.GET.get('1credit') :
		credits+="1"
	if request.GET.get('2credit') :
		credits+="2"
	if request.GET.get('3credit') :
		credits+="3"
	if request.GET.get('4credit') :
		credits+="4"

	if credits :
		creditregex = r'^[A-Z]+[' + credits + r'][0-9A-Za-z]*$'
		subjects.filter(code = creditregex)
		check += "credits "


	subjects.order_by('code')

	returnsubject = [subject.to_dict() for subject in subjects]

	return JsonResponse(returnsubject, safe=False)

@login_required
def add_subject_to_timetable(request, pk):
    table = get_object_or_404(Timetable, pk = pk)
    for Subject in table.subjects.all() :
        sub = Subject
        if(request.POST.get(name) == sub) :
            return JsonResponse("이미 시간표에 있는 과목입니다.", safe = False)
    table.subjects.add(request.POST.get(self))
    return JsonResponse(json.dumps(table))

@login_required
def delete_subject_to_timetable(request, pk):
    table = get_object_or_404(Timetable, pk = pk)
    for Subject in table.subjects.all() :
        sub = Subject
        if(request.POST.get(name) == sub) :
            table.subjects.remove(sub)
            return JsonResponse(json.dumps(table))
    return  JsonResponse("과목을 찾지 못하였습니다. 삭제하지 못했습니다.", safe = False)
