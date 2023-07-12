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

http_address = 'http://127.0.0.1:8000/'

def info_main(request):
    return render(request, "info_main.html")
    
    
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