from django.shortcuts import render, redirect
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

    if not word or word.strip() == "":
        messages.error(request, "Question cannot be empty or only contain spaces！")
        return redirect(http_address + f"word/add?word={word}&tag_name={tag_names}")

    tag_names = tag_names.split()

    # Create or get the conversation
    word, created = Word.objects.get_or_create(word=word)

    # Create the tag
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
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
    # Get the question instance after updating
    Word.objects.filter(id=nid).update(word=word_text)
    word = Word.objects.get(id=nid)

    tag_names = request.POST.getlist("tag_name")
    tag_names = tag_names[0].split()

    # Remove all existing tags for the question
    word.word_tag.clear()

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        word.word_tag.add(tag)

    return redirect(http_address + "word/list/")
