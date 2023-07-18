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
from itertools import groupby
from operator import attrgetter
from django.contrib import messages


http_address = "http://127.0.0.1:8000/"


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

    if not question_text or question_text.strip() == "":
        messages.error(request, "Question cannot be empty or only contain spaces！")
        return redirect(
            http_address
            + f"question/add?answer={answer}&tag_name={' '.join(tag_names)}"
        )

    if not answer or answer.strip() == "":
        messages.error(request, "Answer cannot be empty or only contain spaces！")
        return redirect(
            http_address
            + f"question/add?question={question_text}&tag_name={' '.join(tag_names)}"
        )

    conversation_name = request.POST.get("conversation")
    question_text = request.POST.get("question")
    tag_names = request.POST.get("tag_name").split()
    answer = request.POST.get("answer")
    lmodel_choice = request.POST.get("lmodel")

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
    label_pool = Tag.objects.all()
    if request.method == "GET":
        row_object = Question.objects.filter(id=nid).first()
        lmodel_object = LModel.objects.filter(question=row_object).first()  # Get the LModel object for the question
        if lmodel_object is not None:
            current_answer = lmodel_object.answer
        else:
            current_answer = ""
        return render(
            request,
            "question_edit.html",
            {
                "row_object": row_object,
                "label_pool": label_pool,
                "current_answer": current_answer
            },  # Pass the current answer to the template
        )

    conversation_name = request.POST.get("conversation")
    question_text = request.POST.get("question")
    tag_names = request.POST.get("tag_name").split()
    answer = request.POST.get("answer")
    lmodel_choice = request.POST.get("lmodel")

    if not question_text or question_text.strip() == "":
        messages.error(request, "Question cannot be empty or only contain spaces！")
        return redirect(
            http_address
            + f"question/{nid}/edit?answer={answer}&tag_name={' '.join(tag_names)}"
        )

    if not answer or answer.strip() == "":
        messages.error(request, "Answer cannot be empty or only contain spaces！")
        return redirect(
            http_address
            + f"question/{nid}/edit?question={question_text}&tag_name={' '.join(tag_names)}"
        )

    # Create or get the conversation
    conversation, created = Conversation.objects.get_or_create(name=conversation_name)

    # Get the question instance after updating
    Question.objects.filter(id=nid).update(question=question_text, conversation=conversation)
    question = Question.objects.get(id=nid)

    # Remove all existing tags for the question
    question.question_tag.clear()

    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
        question.question_tag.add(tag)

    LModel.objects.filter(question=question).update(lmodel=lmodel_choice, answer=answer)

    return redirect(http_address + "question/list/")

