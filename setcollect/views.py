from django.shortcuts import render, HttpResponse
from .models import Question, LModel
from django.shortcuts import redirect
from django.contrib import messages

http_address = 'http://127.0.0.1:8000/'

def info_main(request):
    return render(request, "info_main.html")

def test(request):
    return render(request, "test.html")
    
def conversation_list(request):
    return render(request, "conversation_list.html")


def chatbot_view(request):
    return render(request, 'chat_bot.html')

def handle_input(request):
    ai_response = "你好，我是Mudu作文助手。"
    if request.method == 'POST':
        user_input = request.body.decode('utf-8')

        # Process the user input and generate a response
        #在这里连接模型，把模型生成的产出string赋值给ai_response
        ai_response = "你好，我是Mudu作文助手。"

    return HttpResponse(ai_response)



def evaluation(request):
    # 获取所有唯一的问题文本
    unique_questions = Question.objects.values_list('question', flat=True).distinct()

    selected_question_text = request.GET.get('question_text')
    answers_by_model = {}
    current_ratings = {}
    if selected_question_text:
        # 获取每个模型的答案和当前评估值
        for model_choice in LModel.model_choice:
            model_id = model_choice[0]
            answers = LModel.objects.filter(question__question=selected_question_text, lmodel=model_id)
            answers_by_model[model_id] = answers[0].answer if answers else "This question does not have answer from this model."  # 如果没有答案，就使用默认文本
            current_ratings[model_id] = answers[0].evaluation if answers else None

    context = {
        'all_questions': unique_questions,
        'answers_by_model': answers_by_model,
        'selected_question_text': selected_question_text,
        'current_ratings': current_ratings  # 添加当前评估值到上下文
    }

    return render(request, 'evaluation.html', context)

def rate(request):
    if request.method == "POST":
        # 获取问题的文本
        question_text = request.POST.get('question_text')

        # 获取所有的评分值
        rating_1 = request.POST.get('rating_1')
        rating_2 = request.POST.get('rating_2')
        rating_4 = request.POST.get('rating_4')
        rating_9 = request.POST.get('rating_9')

        # 根据问题文本获取相关的问题ID
        related_questions = Question.objects.filter(question=question_text)

        # 更新数据库记录
        for question in related_questions:
            if rating_1:
                LModel.objects.filter(lmodel=1, question=question).update(evaluation=rating_1)
            if rating_2:
                LModel.objects.filter(lmodel=2, question=question).update(evaluation=rating_2)
            if rating_4:
                LModel.objects.filter(lmodel=4, question=question).update(evaluation=rating_4)
            if rating_9:
                LModel.objects.filter(lmodel=9, question=question).update(evaluation=rating_9)

    # 重定向回evaluation页面，以便用户可以继续选择和评价问题
    return redirect(f"/evaluation/?question_text={question_text}")
