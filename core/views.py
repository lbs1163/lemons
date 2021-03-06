from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

from .models import *
from .forms import SignupForm
from .tokens import account_activation_token

import datetime, time
import json
import re

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
    semesters = Semester.objects.all().order_by('-name')
    departments = Department.objects.all().order_by('pk')
    categories = [
        Category.objects.get(category=u"전공필수"),
        Category.objects.get(category=u"전공선택"),
        Category.objects.get(category=u"교양필수"),
        Category.objects.get(category=u"교양선택"),
        Category.objects.get(category=u"기초필수"),
        Category.objects.get(category=u"기초선택"),
        Category.objects.get(category=u"실천필수"),
        Category.objects.get(category=u"실천선택"),
        Category.objects.get(category=u"연구과목"),
        Category.objects.get(category=u"자유선택"),
    ]
    return render(request, "core/index.html",
        {'semesters': semesters,
        'departments': departments,
        'categories': categories})

@login_required
def test(request):
    semesters = Semester.objects.all()
    departments = Department.objects.all()
    categories = Category.objects.all()
    subjects = Subject.objects.all()
    timetables = Timetable.objects.filter(user=request.user)
    return render(request, "core/test.html",
        {'semesters': semesters,
        'departments': departments,
        'categories': categories,
        'subjects': subjects,
        'timetables': timetables})

@login_required
def select_semester(request):
    if request.GET.get('semester') == None:
        raise Http404()
    semester = get_object_or_404(Semester, pk=request.GET.get('semester'))
    timetables = Timetable.objects.filter(user=request.user, semester=semester)
    return JsonResponse([timetable.to_dict() for timetable in timetables], safe=False)

@login_required
def add_timetable(request):
    if request.POST.get('semester') == None:
        raise Http404()
    semester = get_object_or_404(Semester, pk=request.POST.get('semester'))
    add_table = Timetable.objects.create(user=request.user, semester=semester)
    timetables = Timetable.objects.filter(user=request.user, semester=semester)
    return JsonResponse([timetable.to_dict() for timetable in timetables], safe = False)

@login_required
def delete_timetable(request):
    del_table = get_object_or_404(Timetable, pk=request.POST.get('timetable'))
    if del_table.user == request.user:
        del_table.delete()
        timetables = Timetable.objects.filter(user=request.user, semester=del_table.semester)
        return JsonResponse([timetable.to_dict() for timetable in timetables], safe = False)
    else:
        raise Http404()

@login_required
def copy_timetable(request):
    table = get_object_or_404(Timetable, pk=request.POST.get('timetable'))
    if table.user == request.user:
        subjects = table.subjects.all()
        table.pk = None
        table.save()
        table.subjects = subjects
        table.save()
        timetables = Timetable.objects.filter(user=request.user, semester=table.semester)
        return JsonResponse([timetable.to_dict() for timetable in timetables], safe = False)
    else:
        raise Http404()

@login_required
def search_subject(request):
    semester = get_object_or_404(Semester, pk=request.GET.get('semester'))
    subjects = Subject.objects.filter(semester=semester)

    if request.GET.get('q') :
        q = request.GET.get('q')
        aliases = Alias.objects.filter(nickname__contains = q)
        aliaspks = [alias.original.pk for alias in aliases]

        subjects = subjects.filter(Q(professor__contains = q) | Q(name__contains = q) | Q(code__icontains = q) | Q(pk__in = aliaspks))

    hundreds = ""
    if request.GET.get('one_hundred') :
        hundreds+="1"
    if request.GET.get('two_hundred') :
        hundreds+="2"
    if request.GET.get('three_hundred') :
        hundreds+="3"
    if request.GET.get('four_hundred') :
        hundreds+="4"
    if request.GET.get('higher_hundred') :
        hundreds+="56789"

    if hundreds :
        hundredregex = r'^[A-Z]+[' + hundreds + r'][0-9A-Za-z]*$'
        subjects = subjects.filter(code__regex = hundredregex)

    if request.GET.get('department') :
        subjects = subjects.filter(department__pk = request.GET.get('department'))

    if request.GET.get('category') :
        subjects = subjects.filter(category__pk = request.GET.get('category'))

    if request.GET.get('start_time') :
        start_time = request.GET.get('start_time')
        dayoftheweek = start_time[:3]
        stime = datetime.datetime.strptime(start_time[4:], "%H:%M").time()
        end_time = request.GET.get('end_time')
        etime = datetime.datetime.strptime(end_time[4:], "%H:%M").time()
        if dayoftheweek == "mon" :
            periods = Period.objects.filter(mon=True)
        elif dayoftheweek == "tue" :
            periods = Period.objects.filter(tue=True)
        elif dayoftheweek == "wed" :
            periods = Period.objects.filter(wed=True)
        elif dayoftheweek == "thu" :
            periods = Period.objects.filter(thu=True)
        elif dayoftheweek == "fri" :
            periods = Period.objects.filter(fri=True)
        periods = periods.filter(Q(start__gte=stime)&Q(end__lte=etime))
        periodsubjectpks = [period.subject.pk for period in periods]
        subjects = subjects.filter(pk__in = periodsubjectpks)

    credits = ""
    if request.GET.get('one_credit') :
        credits+="1"
    if request.GET.get('two_credit') :
        credits+="2"
    if request.GET.get('three_credit') :
        credits+="3"
    if request.GET.get('four_credit') :
        credits+="4"
    if request.GET.get('higher_credit') :
        credits+="56789"

    if credits :
        creditregex = r'^[0-9][-][0-9][-][' + credits + r']$'
        subjects = subjects.filter(credit__regex = creditregex)

    subjects.order_by('code')

    returnsubject = [subject.to_dict() for subject in subjects]

    return JsonResponse(returnsubject, safe=False)


@login_required
def add_subject_to_timetable(request):
    table = get_object_or_404(Timetable, user=request.user, pk = request.POST.get('timetable'))
    add_subject = get_object_or_404(Subject, pk = request.POST.get('subject'))

    for i in table.subjects.all():
        if(add_subject.pk == i.pk):
            return JsonResponse({'error': '이미 시간표에 있는 과목입니다!'})
        for j in i.period_set.all():
            for k in add_subject.period_set.all():
                if(j.mon == True and k.mon == True):
                    if(k.start >= j.end or k.end <= j.start):
                        pass
                    else:
                        return JsonResponse({'error': '다른 과목과 겹칩니다! 겹치는 과목 : ' + i.name})
                if(j.tue == True and k.tue == True):
                    if(k.start >= j.end or k.end <= j.start):
                        pass
                    else:
                        return JsonResponse({'error': '다른 과목과 겹칩니다! 겹치는 과목 : ' + i.name})
                if(j.wed == True and k.wed == True):
                    if(k.start >= j.end or k.end <= j.start):
                        pass
                    else:
                        return JsonResponse({'error': '다른 과목과 겹칩니다! 겹치는 과목 : ' + i.name})
                if(j.thu == True and k.thu == True):
                    if(k.start >= j.end or k.end <= j.start):
                        pass
                    else:
                        return JsonResponse({'error': '다른 과목과 겹칩니다! 겹치는 과목 : ' + i.name})
                if(j.fri == True and k.fri == True):
                    if(k.start >= j.end or k.end <= j.start):
                        pass
                    else:
                        return JsonResponse({'error': '다른 과목과 겹칩니다! 겹치는 과목 : ' + i.name})
    table.subjects.add(add_subject)
    table.save()
    timetables = Timetable.objects.filter(user=request.user, semester=table.semester)
    return JsonResponse([timetable.to_dict() for timetable in timetables], safe = False)

@login_required
def delete_subject_from_timetable(request):
    table = get_object_or_404(Timetable, user=request.user, pk = request.POST.get('timetable'))
    delete_subject = get_object_or_404(Subject, pk = request.POST.get('subject'))

    for i in table.subjects.all() :
        if(delete_subject.pk == i.pk) :
            table.subjects.remove(i)
            table.save()
            timetables = Timetable.objects.filter(user=request.user, semester=table.semester)
            return JsonResponse([timetable.to_dict() for timetable in timetables], safe = False)
    return  JsonResponse({'error': '이미 시간표에 없는 과목입니다!'})


def subject_detail(request, subjectPK):
    subject = get_object_or_404(Subject, pk = subjectPK)
    #get period
    period = Period.objects.filter(subject = subject)

    return render(request, 'core/subject_detail.html', {'subject': subject, 'period': period})

def aboutus(request):
    return render(request, 'core/aboutus.html', {})

def howtouse(request):
    return render(request, 'core/howtouse.html', {})
