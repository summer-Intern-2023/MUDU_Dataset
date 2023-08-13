from django.shortcuts import render, HttpResponse
from .models import Question, LModel

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
    if selected_question_text:
        # 获取每个模型的答案
        for model_choice in LModel.model_choice:
            model_id = model_choice[0]
            answers = LModel.objects.filter(question__question=selected_question_text, lmodel=model_id)
            answers_by_model[model_id] = answers[0].answer if answers else "This question does not have answer from this model."  # 如果没有答案，就使用默认文本

    context = {
        'all_questions': unique_questions,
        'answers_by_model': answers_by_model,
        'selected_question_text': selected_question_text
    }

    return render(request, 'Evaluation.html', context)

