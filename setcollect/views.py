from django.shortcuts import render, HttpResponse, redirect
import django.http
from setcollect.models import UserInfo, Question, LModel, Tag
from django import forms

http_address = 'http://127.0.0.1:8000/'
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
        return redirect(http_address + 'info/main')
    


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
    return redirect(http_address + "info/list/")

def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect(http_address + "info/list/") 

def info_edit(request, nid):
    if request.method == "GET":
        row_object = UserInfo.objects.filter(id = nid).first()
        return render(request, 'info_edit.html', {"row_object":row_object})
    
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    UserInfo.objects.filter(id=nid).update(name=user)
    UserInfo.objects.filter(id=nid).update(password=pwd)

    return redirect(http_address + "info/list/")

#---#

#--data collection--#
def question_list(request):
    #get all datas in sql
    data_list = Question.objects.prefetch_related("lmodel_set", "tag_set").all()

    
    #tansform into html and return
    return render(request,"question_list.html",{"data_list":data_list})
    

def question_add(request):
    if request.method == "GET":
        return render(request, 'question_add.html')
    
    question_text = request.POST.get("question")
    tag_names = request.POST.getlist("tag_name")
    tag_names = tag_names[0].split(" ")
    print(tag_names)
    
    question = Question.objects.create(question = question_text)

    lmodel_choice = request.POST.get("lmodel")
    answer = request.POST.get("answer")

    # Create the LModel
    LModel.objects.create(lmodel=lmodel_choice, answer=answer, question=question)

    # Create the tag
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        tag.question.add(question)
    
    return redirect(http_address + "question/list/")

def question_delete(request):
    nid = request.GET.get('nid')
    Question.objects.filter(id = nid).delete()
    return redirect(http_address + "question/list/")

def question_edit(request, nid):
    if request.method == "GET":
        row_object = Question.objects.filter(id = nid).first()
        return render(request, 'question_edit.html', {"row_object": row_object})
    
    question_text = request.POST.get("question")
    # Get the question instance after updating
    Question.objects.filter(id=nid).update(question=question_text)
    question = Question.objects.get(id=nid)

    tag_names = request.POST.getlist("tag_name")
    tag_names = tag_names[0].split(" ")

    # Remove all existing tags for the question
    question.tag_set.clear()

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        tag.question.add(question)

    return redirect(http_address + "question/list/")
