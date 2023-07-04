from django.shortcuts import render, HttpResponse, redirect
import django.http

from setcollect.models import UserInfo, Question, LModel
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )
    password = forms.CharField(
        label="密码",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )
    
    

#---#
def info_main(request):
    return render(request, 'info_main.html')
#---#

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html",{'form':form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_object = UserInfo.objects.filter(name = form.cleaned_data['username'], password = form.cleaned_data['password']).first()
        
        if not user_object:
            form.add_error("username", "用户名错误")
            form.add_error("password", "密码错误")
            return render(request, "login.html",{'form':form})

        request.session["info"] = {'id':user_object.id, 'name':user_object.name}
        return redirect('http://127.0.0.1:8000/info/main')
    


#--user manage--#
def info_list(request):
    #get all datas in sql
    data_list = UserInfo.objects.all()
    
    #tansform into html and return
    return render(request,"info_list.html",{"data_list":data_list})

def info_add(request):
    if request.method == "GET":
        return render(request, 'info_add.html')
    
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")

    UserInfo.objects.create(name = user, password = pwd)
    return redirect("http://127.0.0.1:8000/info/list/")

def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect("http://127.0.0.1:8000/info/list/") 

def info_edit(request, nid):
    if request.method == "GET":
        row_object = UserInfo.objects.filter(id = nid).first()
        return render(request, 'info_edit.html', {"row_object":row_object})
    
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    UserInfo.objects.filter(id=nid).update(name=user)
    UserInfo.objects.filter(id=nid).update(password=pwd)

    return redirect("http://127.0.0.1:8000/info/list/")

#---#

#--data collection--#
def question_list(request):
    #get all datas in sql
    data_list = Question.objects.all()
    
    #tansform into html and return
    return render(request,"question_list.html",{"data_list":data_list})

def question_add(request):
    if request.method == "GET":
        return render(request, 'question_add.html')
    
    question = request.POST.get("question")
    tag_name = request.POST.get("tag_name")

    Question.objects.create(question = question, tag_name = tag_name)
    return redirect("http://127.0.0.1:8000/question/list/")

def question_delete(request):
    nid = request.GET.get('nid')
    Question.objects.filter(id = nid).delete()
    return redirect("http://127.0.0.1:8000/question/list/")

def question_edit(request, nid):
    if request.method == "GET":
        row_object = Question.objects.filter(id = nid).first()
        return render(request, 'question_edit.html', {"row_object":row_object})
    
    question = request.POST.get("question")
    tag_name = request.POST.get("tag_name")
    Question.objects.filter(id=nid).update(question=question)
    Question.objects.filter(id=nid).update(tag_name=tag_name)

    return redirect("http://127.0.0.1:8000/question/list/")


#---#
# LModel solution management
def lmodel_list(request, nid):
    #get all datas in sql
    data = Question.objects.get(question_id = nid)
    module_list = data.LModel_set.all()

    #tansform into html and return
    return render(request, "lmodel_list.html",{"data_list":module_list})

def lmodel_add(request, nid):
    if request.method == "GET":
        return render(request, 'lmodel_add.html')
    
    lmodel = request.POST.get("lmodule")
    answer = request.POST.get("answer")
    Question.objects.get(question_id = nid).LModel_set.create(lmodel = lmodel, answer = answer)
    return redirect("http://127.0.0.1:8000/lmodel/list/%s" % nid)

#delete this method
def lmodel_delete(request, nid):
    lmodel = request.POST.get("lmodule")
    Question.objects.get(question_id = nid).LModel_set.filter(id = lmodel).delete()
    return redirect("http://127.0.0.1:8000/lmodel/list/")

def lmodel_edit(request, nid):
    if request.method == "GET":
        row_object = Question.objects.get(question_id = nid).LModel_set.get(id = nid)
        return render(request, 'lmodel_edit.html', {"row_object":row_object})
    
    lmodel = request.POST.get("lmodule")
    answer = request.POST.get("answer")
    Question.objects.get(question_id = nid).LModel_set.filter(id = nid).update(lmodel = lmodel)
    Question.objects.get(question_id = nid).LModel_set.filter(id = nid).update(answer = answer)

    return redirect("http://127.0.0.1:8000/lmodel/list/")