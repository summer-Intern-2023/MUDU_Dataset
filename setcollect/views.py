from django.shortcuts import render, HttpResponse, redirect


http_address = 'http://127.0.0.1:8000/'

def info_main(request):
    return render(request, "info_main.html")
    
    
