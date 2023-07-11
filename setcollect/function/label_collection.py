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



def label_list(request):
    # get all datas in sql
    data_list = Tag.objects.annotate(num_questions=Count("question")).all()

    # tansform into html and return
    return render(request, "label_list.html", {"data_list": data_list})



def label_add(request):
    if request.method == "GET":
        return render(request, "label_add.html")

    tag_name = request.POST.get("tag_name")
    Tag.objects.create(tag_name=tag_name)

    return redirect(http_address + "label/list/")


def label_delete(request):
    nid = request.GET.get("nid")
    Tag.objects.filter(id=nid).delete()
    return redirect(http_address + "label/list/")



def search_by_label(request):
    if request.method == "GET":
        all_tags = Tag.objects.values_list("tag_name", flat=True)
        return render(request, "label_search.html", {"all_tags": all_tags})

    return redirect(http_address + "label/list/")



def search_search(request):
    if request.method == "GET":
        search_tag = request.GET.get("tag_name", "")
        if search_tag:
            tag = Tag.objects.filter(tag_name__icontains=search_tag).first()
            if tag:
                questions = tag.question.all()
            else:
                questions = Question.objects.none()  # Return an empty queryset
        else:
            questions = Question.objects.none()  # Return an empty queryset

        return render(request, "search_results.html", {"questions": questions})
