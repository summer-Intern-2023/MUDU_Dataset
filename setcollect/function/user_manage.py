from django.shortcuts import render, redirect
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
from django.contrib import messages


http_address = "192.168.132.168/"


class LoginForm(forms.Form):
    username = forms.CharField(
        label="User name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_object = UserInfo.objects.filter(
            name=form.cleaned_data["username"], password=form.cleaned_data["password"]
        ).first()

        if not user_object:
            form.add_error("username", "Username error")
            form.add_error("password", "Password error")
            return render(request, "login.html", {"form": form})

        request.session["info"] = {"id": user_object.id, "name": user_object.name}
        return redirect(http_address + "info/main")


def info_list(request):
    # get all datas in sql
    data_list = UserInfo.objects.all()

    # tansform into html and return
    return render(request, "info_list.html", {"data_list": data_list})


def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html")

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    role = request.POST.get("role")

    if not user or " " in user:
        messages.error(request, "Username cannot be empty or contain spaces！")
        return redirect(http_address + f"info/add?pwd={pwd}&role={role}")

    if not pwd or " " in pwd:
        messages.error(request, "Password cannot be empty or contain spaces！")
        return redirect(http_address + f"info/add?user={user}&role={role}")

    # 检查用户名是否已存在
    existing_user = UserInfo.objects.filter(name=user).first()
    if existing_user:
        messages.error(request, "Username already exist!")
        return redirect(
            http_address + f"info/add?user={user}&pwd={pwd}&role={role}"
        )  # 重定向回编辑页面

    UserInfo.objects.create(name=user, password=pwd, role=role)

    return redirect(http_address + "info/list/")


def info_delete(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect(http_address + "info/list/")


def info_edit(request, nid):
    if request.method == "GET":
        row_object = UserInfo.objects.filter(id=nid).first()
        return render(request, "info_edit.html", {"row_object": row_object})

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    role = request.POST.get("role")

    if not user or " " in user:
        messages.error(request, "Username cannot be empty or contain spaces！")
        return redirect(http_address + f"info/{nid}/edit/")

    if not pwd or " " in pwd:
        messages.error(request, "Password cannot be empty or contain spaces！")
        return redirect(http_address + f"info/{nid}/edit/")

    # 检查用户名是否已存在
    existing_user = UserInfo.objects.filter(name=user).exclude(id=nid).first()
    if existing_user:
        messages.error(request, "Username already exist!")
        return redirect(http_address + f"info/{nid}/edit/")  # 重定向回编辑页面

    UserInfo.objects.filter(id=nid).update(name=user, password=pwd, role=role)

    return redirect(http_address + "info/list/")


def user_list(request):
    # get all datas in sql
    data_list = Question.objects.prefetch_related("lmodel_set").all()
    for data in data_list:
        print(data)

    # tansform into html and return
    return render(request, "user_list.html", {"data_list": data_list})
