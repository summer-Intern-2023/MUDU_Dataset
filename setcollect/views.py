from django.shortcuts import render, HttpResponse, redirect


http_address = 'http://192.168.132.168/'

def info_main(request):
    return render(request, "info_main.html")

def test(request):
    return render(request, "test.html")
    
    
