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
    unique_questions = Question.objects.values_list('question', flat=True).distinct()

    selected_question_text = request.GET.get('question_text')
    if selected_question_text:
        answers_by_model = {}
        for model_choice in LModel.model_choice:
            model_id = model_choice[0]
            answers_by_model[model_id] = LModel.objects.filter(question__question=selected_question_text, lmodel=model_id)
    else:
        answers_by_model = {}

    context = {
        'all_questions': unique_questions,
        'answers_by_model': answers_by_model,
        'selected_question_text': selected_question_text
    }

    return render(request, 'evaluation.html', context)

