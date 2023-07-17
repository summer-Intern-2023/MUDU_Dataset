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

    for (
        title_object,
        emotion_list,
        words_list,
    ) in mapping.mapping_words_to_titles():
        for word in words_list:
            word_object = Word.objects.filter(word=word)
            if word_object:
                title_object.words.add(word_object)

        for sentence in mapping.mapping_words_to_sentences(
            title_object.title, words_list, emotion_list
        ):
            sentence_object = Sentences.objects.create(sentences=sentence)
            sentence_object.title = title_object
            for word in words_list:
                word_object = Word.objects.filter(word=word)
                if word_object:
                    sentence_object.words.add(word_object)

        title_data.append(
            {
                "title": title_object.title,
                "words": [word.word for word in title_object.words.all()],
                "sentences": [
                    sentence.sentences
                    for sentence in Sentences.objects.filter(title=title_object)
                ],
            }
        )
    return render(request, "title_list.html", {"titles": title_data})


def title_add(request):
    if request.method == "GET":
        return render(request, "title_add.html")

    title = request.POST.get("title")
    Title.objects.create(title=title)

    return redirect(http_address + "title/list/")


def title_delete(request):
    nid = request.GET.get("nid")
    Title.objects.filter(id=nid).delete()
    return redirect(http_address + "title/list/")


def title_edit(request, nid):
    if request.method == "GET":
        row_object = Title.objects.filter(id=nid).first()
        return render(request, "title_edit.html", {"row_object": row_object})

    title = request.POST.get("title")
    Title.objects.filter(id=nid).update(title=title)
    return redirect(http_address + "title/list/")
