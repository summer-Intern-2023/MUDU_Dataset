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
    titles = Title.objects.all()
    title_data = []
    mapping.mapping_titles_to_words()

    for title in titles:
        sentences = Sentences.objects.filter(title=title)
        sentence_texts = [sentence.sentences for sentence in sentences]

        words = []
        for sentence in sentences:
            related_words = sentence.words.all()
            words.extend([word.word for word in related_words])

        title_data.append(
            {
                "title": title,
                "sentences": sentence_texts,
                "words": list(set(words)),  # Remove duplicates using set
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
    sentence_pool = Sentences.objects.all()
    if request.method == "GET":
        row_object = Title.objects.filter(id=nid).first()
        return render(
            request, 
            "title_edit.html", 
            {"row_object": row_object, "sentences_pool": sentence_pool}
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
