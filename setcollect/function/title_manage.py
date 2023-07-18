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

http_address = "http://127.0.0.1:8000/"

import mapping


def title_list(request):
    title_data = []

    for title in Title.objects.all():
        (
            title_object,
            emotion_list,
            words_list,
            sentences_list,
            skip,
        ) = mapping.mapping(title)
        if skip:
            print(title.title, "has been skipped")
            title_data.append(
                {
                    "title": title_object,
                    "word": [word for word in title_object.words.all()],
                    "sentences": [
                        sentence for sentence in title_object.sentences.all()
                    ],
                }
            )
            continue
        else:
            print(title.title, "has been processed")
            for word in words_list:
                try:
                    word_object = Word.objects.get(word=word)
                    if word_object:
                        title_object.words.add(word_object)
                except Word.DoesNotExist:
                    print("words does not exist.")

            for sentence in sentences_list:
                sentence_object = Sentences.objects.create(sentences=sentence)
                title_object.sentences.add(sentence_object)
                for word in words_list:
                    try:
                        word_object = Word.objects.get(word=word)
                        if word_object:
                            title_object.words.add(word_object)
                    except Word.DoesNotExist:
                        print("sentences does not exist.")

        title_data.append(
            {
                "title": title_object,
                "word": [word for word in title_object.words.all()],
                "sentences": [sentence for sentence in title_object.sentences.all()],
            }
        )
    return render(request, "title_list.html", {"titles": title_data})


def title_add(request):
    if request.method == "GET":
        return render(request, "title_add.html")

    title = request.POST.get("title")
    Title.objects.get_or_create(title=title)

    return redirect(http_address + "title/list/")


def title_delete(request):
    nid = request.GET.get("nid")
    Title.objects.filter(id=nid).delete()
    return redirect(http_address + "title/list/")


def title_edit(request, nid):
    sentence_pool = Sentences.objects.all()
    if request.method == "GET":
        row_object = Title.objects.filter(id=nid).first()
        return render(
            request,
            "title_edit.html",
            {"row_object": row_object, "sentences_pool": sentence_pool},
        )

    title = request.POST.get("title")
    sentences = request.POST.get("sentences")
    sentences = sentences[0].split()

    words = request.POST.get("words")
    words = words[0].split()

    Title.objects.filter(id=nid).update(title=title)

    sentences.clear()

    for sentence in sentences:
        sentences, created = Sentences.objects.get_or_create(sentences=sentence)
        title.title_sentences.add(sentences)
    return redirect(http_address + "title/list/")
