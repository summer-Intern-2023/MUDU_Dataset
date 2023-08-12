from django.shortcuts import render, HttpResponse


http_address = 'http://127.0.0.1:8000/'

def info_main(request):
    return render(request, "info_main.html")

def test(request):
    return render(request, "test.html")
    
def conversation_list(request):
    return render(request, "conversation_list.html")

