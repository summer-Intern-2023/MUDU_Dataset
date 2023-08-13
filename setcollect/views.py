from django.shortcuts import render, HttpResponse


http_address = 'http://127.0.0.1:8000/'

def info_main(request):
    return render(request, "info_main.html")

def test(request):
    return render(request, "test.html")
    
def conversation_list(request):
    return render(request, "conversation_list.html")

   
def chatbot_view(request):
    return render(request, 'Chatbot.html')

def chatbot_view(request):
    return render(request, 'chatbot.html')

def handle_input(request):
    ai_response = "你好，我是木渎作文助手。"
    if request.method == 'POST':
        user_input = request.body.decode('utf-8')

        # Process the user input and generate a response
        #在这里连接模型，把模型生成的产出string赋值给ai_response
        ai_response = "你好，我是木渎作文助手。"

    return HttpResponse(ai_response)
