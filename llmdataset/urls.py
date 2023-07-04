"""
URL configuration for llmdataset project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from setcollect import views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    #user manage
    path('login/',views.login),
    path('info/list/', views.info_list),
    path('info/add/', views.info_add),
    path('info/delete/', views.info_delete),
    path('info/<int:nid>/edit/', views.info_edit),
    path('info/main/', views.info_main),

    #question manage
    path('question/list/', views.question_list),
    path('question/add/', views.question_add),
    path('question/delete/', views.question_delete),
    path('question/<int:nid>/edit/', views.question_edit),
    
]
