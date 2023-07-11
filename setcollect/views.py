from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from setcollect.models import (
    UserInfo,
    Conversation,
    Question,
    LModel,
    Tag,
    Title,
    Sentences,
    Word,
)
from django import forms
from itertools import groupby
from operator import attrgetter
from django.contrib import messages


def info_main(request):
    return render(request, "info_main.html")
