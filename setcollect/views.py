from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from setcollect.models import UserInfo, Conversation, Question, LModel, Tag
from django import forms
from itertools import groupby
from operator import attrgetter
from django.contrib import messages

http_address = 'http://127.0.0.1:8000/'

class LoginForm(forms.Form):
    username = forms.CharField(
        label="User name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )
    password = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )


def info_main(request):
    return render(request, 'info_main.html')