from django.conf.urls import url
from . import views
from core.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^signup/$', Signup.as_view(), name='signup'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', Activate.as_view(), name='activate'),
	url(r'^$', views.timetable, name='timetable'),
	url(r'^test/$', views.test, name='test'),
	# select semester
	# get method로 요청이 들어오면 사용자 로그인 체크 (login_required decorator 검색해보셈)
	# URL query: semester (학기 모델의 pk가 들어있음)
	# example URL: select_semester/?semester=3
	# user가 소유한 timetable 중에서 semester가 일치하는 것들을 JSON 형식으로 return
	url(r'^select_semester/$', views.select_semester, name='select_semester'),
	# add timetable
	# post method로 요청이 들어오면 사용자 로그인 체크
	# POST data: semester (학기 모델의 pk가 들어있음)
	# 해당 semester로 user가 소유한 timetable을 새로 생성
	# 생성 후 성공시 새로 생성된 timetable의 내용을 JSON 형식으로 return
	url(r'^add_timetable/$', views.add_timetable, name='add_timetable'),
	# delete timetable
	# post method로 요청이 들어오면 사용자 로그인 체크
	# POST data: timetable (시간표 모델의 pk가 들어있음)
	# 해당 timetable이 user 소유인지 확인
	# user 소유가 맞으면 timetable 삭제 후 성공 메시지를 JSON으로 return
	# user 소유가 아니면 실패 메시지를 JSON으로 return
	url(r'^delete_timetable/$', views.delete_timetable, name='delete_timetable'),
	# copy timetable
	# post method로 요청이 들어오면 사용자 로그인 체크
	# POST data: timetable (시간표 모델의 pk가 들어있음)
	# 해당 timetable이 user 소유인지 확인
	# user 소유가 맞으면 새로운 timetable을 만듬
	# 기존 timetable이 갖는 과목을 새로운 timetable도 갖게 만듬
	# 성공하면 새로 생성된 timetable의 내용을 JSON 형식으로 return
	# 실패하면 실패 메시지를 JSON으로 return
	url(r'^copy_timetable/$', views.copy_timetable, name='copy_timetable'),
	# search subject
	# get method로 요청이 들어오면 사용자 로그인 체크
	# URL query: q, hundreds, department, category, start_time, end_time, credit
	# 검색 조건에 따라 해당 값이 쿼리에 없을 수도 있음
	# ex) copy_timetable/?q=윤은영&hundreds=1
	# 검색 조건에 맞는 subject들을 학수번호로 정렬하여 JSON으로 return
	url(r'^search_subject/$', views.search_subject, name='search_subject'),
	# add subject to timetable
	# post method로 요청이 들어오면 사용자 로그인 체크
	# POST data: timetable, subject (시간표 모델과 과목 모델의 pk가 들어있음)
	# 해당 timetable이 user 소유인지 확인
	# user 소유가 맞으면 해당 subject를 추가
	# 성공하면 변경된 timetable의 내용을 JSON 형식으로 return
	# 실패하면 실패 메시지를 JSON으로 return
	url(r'^add_subject_to_timetable/$', views.add_subject_to_timetable, name='add_subject_to_timetable'),
	# delete subject to timetable
	# post method로 요청이 들어오면 사용자 로그인 체크
	# POST data: timetable, subject (시간표 모델과 과목 모델의 pk가 들어있음)
	# 해당 timetable이 user 소유인지 확인
	# 해당 subject가 해당 timetable에 포함되어 있는지 확인
	# user 소유가 맞고 해당 subject가 있으면 해당 subject를 삭제
	# 성공하면 변경된 timetable의 내용을 JSON 형식으로 return
	# 실패하면 실패 메시지를 JSON으로 return
	url(r'^delete_subject_from_timetable/$', views.delete_subject_from_timetable, name='delete_subject_from_timetable'),




	url(r'^subject/(?P<subjectPK>[0-9]+)/$', views.subject_detail, name='subject_detail'),
]