from django.shortcuts import render, redirect
from django.utils.http import urlencode
from setcollect.models import (
    Tag,
    Word,
)
from django.contrib import messages

http_address = "http://127.0.0.1:8000/"

# --word manage--#


def word_list(request):
    # get all datas in sql
    word = Word.objects.all().prefetch_related("word_tag").order_by("id")

    # tansform into html and return
    return render(request, "word_list.html", {"data_list": word})


def word_add(request):
    label_pool = Tag.objects.all()
    if request.method == "GET":
        return render(request, "word_add.html", {"label_pool": label_pool})
    
    word = request.POST.get("word")
    tag_names = request.POST.get("tag_name")
    #tag_classification = request.POST.get("tag_classification")
    
    
    if not word or word.strip() == "":
        messages.error(request, "Word cannot be empty or only contain spaces!")
        word_param = word or ''
        tag_names_param = tag_names or ''
        return render(request, "word_add.html")

    # 检查word是否已存在
    existing_Word = Word.objects.filter(word=word).first()
    if existing_Word:
        word_param = '' if word is None else word
        messages.error(request, "Word already exists!")
        return redirect(http_address + f"word/add/?word={urlencode({'word': word_param})}/")

    tag_names = tag_names.split()

    # Create or get the conversation
    word, created = Word.objects.get_or_create(word=word)

    # Create the tag
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(
            tag_name=tag_name
        )
        word.word_tag.add(tag)


    return redirect(http_address + "word/list/")



def word_delete(request):
    nid = request.GET.get("nid")
    Word.objects.filter(id=nid).delete()
    return redirect(http_address + "word/list/")


def word_edit(request, nid):
    label_pool = Tag.objects.all()
    if request.method == "GET":
        row_object = Word.objects.filter(id=nid).first()
        return render(
            request,
            "word_edit.html",
            {"row_object": row_object, "label_pool": label_pool},
        )

    word_text = request.POST.get("word")
    word = Word.objects.filter(id=nid).first()

    #tag_classification = request.POST.get("tag_classification")

    if not word_text or word_text.strip() == "":
        messages.error(request, "Word cannot be empty or only contain spaces!")
        return redirect(http_address + f"word/{nid}/edit/")

    # 检查word是否已存在，排除当前正在编辑的word
    existing_word = Word.objects.filter(word=word_text).exclude(id=nid).first()
    if existing_word:
        messages.error(request, "Word already exist!")
        return redirect(http_address + f"word/{nid}/edit/")  # 重定向回编辑页面

    # Update the word text
    word.word = word_text
    word.save()

    # Update the tags
    tag_names = request.POST.getlist("tag_name")
    tag_names = tag_names[0].split()

    # Clear existing tags
    word.word_tag.clear()

    # Add selected tags
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(
            tag_name=tag_name
        )
        # if not created:
        word.word_tag.add(tag)

    return redirect(http_address + "word/list/")
