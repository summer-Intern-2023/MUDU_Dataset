from django.shortcuts import render, HttpResponse, redirect
import django.http
from django.db.models import Count
from setcollect.models import UserInfo, Question, LModel, Tag
from django import forms

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
            form.add_error("username", "Username error")
            form.add_error("password", "Password error")
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
    role = request.POST.get("role")

    UserInfo.objects.create(name = user, password = pwd, role = role)
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
    role = request.POST.get("role")
    
    UserInfo.objects.filter(id=nid).update(name=user)
    UserInfo.objects.filter(id=nid).update(password=pwd)
    UserInfo.objects.filter(id=nid).update(role=role)
    
    return redirect(http_address + "info/list/")

def user_list(request):
    #get all datas in sql
    data_list = Question.objects.prefetch_related("lmodel_set").all()
    for data in data_list:    
        print(data)
        
    
    #tansform into html and return
    return render(request,"user_list.html",{"data_list":data_list})
    

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
    tag_names = tag_names[0].split()
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
    tag_names = tag_names[0].split()

    # Remove all existing tags for the question
    question.tag_set.clear()

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        tag.question.add(question)

    return redirect(http_address + "question/list/")


#--label collection--#
def label_list(request):
    #get all datas in sql
    data_list = Tag.objects.annotate(num_questions=Count('question')).all()

    #tansform into html and return
    return render(request,"label_list.html",{"data_list":data_list})

def label_add(request):
    if request.method == "GET":
        return render(request, 'label_add.html')

    tag_name = request.POST.get("tag_name")
    Tag.objects.create(tag_name = tag_name)

    return redirect(http_address + "label/list/")


def label_delete(request):
    nid = request.GET.get('nid')
    Tag.objects.filter(id = nid).delete()
    return redirect(http_address + "label/list/")




