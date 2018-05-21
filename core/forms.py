#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label=u'이름')
    last_name = forms.CharField(max_length=30, label=u'성')
    email = forms.EmailField(max_length=254, label=u'POVIS 이메일', help_text=u'POVIS 이메일만 가능합니다.')
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = u'아이디'
        self.fields['password1'].label = u'비밀번호'
        self.fields['password2'].label = u'비밀번호 재확인'

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if data and User.objects.filter(email=data).exclude(username=username).exists():
            raise forms.ValidationError(u"이미 사용중인 이메일입니다.")
        domain = data.split('@')[1]
        if domain != "postech.ac.kr":
            raise forms.ValidationError(u"POVIS 이메일만 가능합니다.")
        return data