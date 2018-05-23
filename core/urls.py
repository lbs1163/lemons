from django.conf.urls import url
from . import views
from core.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^signup/$', Signup.as_view(), name='signup'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),


	url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='core/password_reset_form.html'), name="password_reset_form"),
	url(r'^password_reset/done$', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name="password_reset_done"),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name="password_reset_confirm"),
	url(r'^reset/done$', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name="password_reset_complete"),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', Activate.as_view(), name='activate'),

	
	url(r'^$', views.timetable, name='timetable'),
	url(r'^test/$', views.test, name='test'),
	url(r'^select_semester/$', views.select_semester, name='select_semester'),
	url(r'^add_timetable/$', views.add_timetable, name='add_timetable'),
	url(r'^delete_timetable/$', views.delete_timetable, name='delete_timetable'),
	url(r'^copy_timetable/$', views.copy_timetable, name='copy_timetable'),
	url(r'^search_subject/$', views.search_subject, name='search_subject'),
	url(r'^add_subject_to_timetable/$', views.add_subject_to_timetable, name='add_subject_to_timetable'),
	url(r'^delete_subject_from_timetable/$', views.delete_subject_from_timetable, name='delete_subject_from_timetable'),
	url(r'^subject/(?P<subjectPK>[0-9]+)/$', views.subject_detail, name='subject_detail'),
	url(r'^aboutus/$', views.aboutus, name='aboutus'),
	url(r'^howtouse/$', views.howtouse, name='howtouse'),
]