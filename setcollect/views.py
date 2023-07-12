from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count
from setcollect.models import UserInfo, Conversation, Question, LModel, Tag, Word
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

#---#
def info_main(request):
    return render(request, 'info_main.html')

def test(request):
    return render(request, 'test.html')
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
    
    if not user or " " in user: 
        messages.error(request, 'Username cannot be empty or contain spaces！') 
        return redirect(http_address + f"info/add?pwd={pwd}&role={role}") 
    
    if not pwd or " " in pwd: 
        messages.error(request, 'Password cannot be empty or contain spaces！') 
        return redirect(http_address + f"info/add?user={user}&role={role}")
    
    # 检查用户名是否已存在
    existing_user = UserInfo.objects.filter(name=user).first()
    if existing_user:
        messages.error(request, 'Username already exist!')
        return redirect(http_address + f"info/add?user={user}&pwd={pwd}&role={role}") # 重定向回编辑页面

    
    UserInfo.objects.create(name=user, password=pwd, role=role)

    return redirect(http_address + "info/list/")
    

def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect(http_address + "info/list/") 


def info_edit(request, nid):
    if request.method == "GET":
        row_object = UserInfo.objects.filter(id=nid).first()
        return render(request, 'info_edit.html', {"row_object": row_object})

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    role = request.POST.get("role")
    
    if not user or " " in user: 
        messages.error(request, 'Username cannot be empty or contain spaces！') 
        return redirect(http_address + f"info/{nid}/edit/")
    
    if not pwd or " " in pwd: 
        messages.error(request, 'Password cannot be empty or contain spaces！') 
        return redirect(http_address + f"info/{nid}/edit/")
    
    # 检查用户名是否已存在
    existing_user = UserInfo.objects.filter(name=user).exclude(id=nid).first()
    if existing_user:
        messages.error(request, 'Username already exist!')
        return redirect(http_address + f"info/{nid}/edit/") # 重定向回编辑页面

    UserInfo.objects.filter(id=nid).update(name=user, password=pwd, role=role)

    return redirect(http_address + "info/list/")

def user_list(request):
    #get all datas in sql
    data_list = Question.objects.prefetch_related("lmodel_set").all()
    for data in data_list:    
        print(data)
        
    
    #tansform into html and return
    return render(request,"user_list.html",{"data_list":data_list})


# ---#


# --data collection--#
def question_list(request):
    questions = (
        Question.objects.all()
        .prefetch_related("question_tag", "lmodel_set", "conversation")
        .order_by("conversation__id")
    )

    # Group questions by conversation
    conversations = {
        k: list(g) for k, g in groupby(questions, key=attrgetter("conversation.name"))
    }

    # Generate indices within each conversation
    for conversation in conversations.values():
        for i, question in enumerate(conversation, start=1):
            question.index_within_conversation = i

    # Flatten list of conversations back into list of questions
    data_list = [
        question for conversation in conversations.values() for question in conversation
    ]

    return render(request, "question_list.html", {"data_list": data_list})



def question_add(request):
    label_pool = Tag.objects.all()
    if request.method == "GET":
        return render(request, "question_add.html", {"label_pool": label_pool})

    conversation_name = request.POST.get("conversation")
    question_text = request.POST.get("question")
    tag_names = request.POST.get("tag_name")
    answer = request.POST.get("answer")
    lmodel_choice = request.POST.get("lmodel")

    if not question_text or question_text.strip() == "":
        messages.error(request, "Question cannot be empty or only contain spaces！")
        return redirect(
            http_address + f"question/add?answer={answer}&tag_name={tag_names}"
        )

    if not answer or answer.strip() == "":
        messages.error(request, "Answer cannot be empty or only contain spaces！")
        return redirect(
            http_address + f"question/add?question={question_text}&tag_name={tag_names}"
        )

    tag_names = tag_names.split()

    # Create or get the conversation
    conversation, created = Conversation.objects.get_or_create(name=conversation_name)

    question = Question.objects.create(
        question=question_text, conversation=conversation
    )

    # Create the LModel
    LModel.objects.create(lmodel=lmodel_choice, answer=answer, question=question)

    # Create the tag
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        question.question_tag.add(tag)

    return redirect(http_address + "question/list/")


def question_delete(request):
    nid = request.GET.get("nid")
    Question.objects.filter(id=nid).delete()
    return redirect(http_address + "question/list/")


def question_edit(request, nid):
    if request.method == "GET":
        row_object = Question.objects.filter(id=nid).first()
        return render(request, "question_edit.html", {"row_object": row_object})

    question_text = request.POST.get("question")
    # Get the question instance after updating
    Question.objects.filter(id=nid).update(question=question_text)
    question = Question.objects.get(id=nid)

    tag_names = request.POST.getlist("tag_name")
    tag_names = tag_names[0].split()

    # Remove all existing tags for the question
    question.question_tag.clear()

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        question.question_tag.add(tag)

    lmodel_choice = request.POST.get("lmodel")
    answer = request.POST.get("answer")
    LModel.objects.filter(question=question).update(lmodel=lmodel_choice, answer=answer)

    return redirect(http_address + "question/list/")


# --label collection--#

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
    
    
# --word collection--#

def word_list(request):
    #get all datas in sql
    word = (
        Word.objects.all()
        .prefetch_related("word_tag")
        .order_by("id")
    )
    
    #tansform into html and return
    return render(request,"word_list.html",{"data_list":word})

def word_add(request):
    label_pool = Tag.objects.all()
    if request.method == "GET":
        return render(request, "word_add.html", {"label_pool": label_pool})

    word = request.POST.get("word")
    tag_names = request.POST.get("tag_name")


    if not word or word.strip() == "":
        messages.error(request, "Question cannot be empty or only contain spaces！")
        return redirect(
            http_address + f"word/add?word={word}&tag_name={tag_names}"
        )

    tag_names = tag_names.split()

    # Create or get the conversation
    word, created = Word.objects.get_or_create(word=word)

    # Create the tag
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        word.word_tag.add(tag)

    return redirect(http_address + "word/list/")