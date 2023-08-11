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

import sys

sys.path.append("setcollect//function")
from setcollect import views
from setcollect.function import (
    user_manage,
    question_manage,
    title_manage,
    label_collection,
    word_manage,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # main views
    path("info/main/", views.info_main),
    path("test/", views.test),
    # user manage
    path("login/", user_manage.login),
    path("info/list/", user_manage.info_list),
    path("info/add/", user_manage.info_add),
    path("info/delete/", user_manage.info_delete),
    path("info/<int:nid>/edit/", user_manage.info_edit),
    path("user/list/", user_manage.user_list),
    # question manage
    path("question/list/", question_manage.question_list),
    path("question/add/", question_manage.question_add),
    path("question/delete/", question_manage.question_delete),
    path("question/<int:nid>/edit/", question_manage.question_edit),
    # label manage
    path("label/list/", label_collection.label_list),
    path("label/add/", label_collection.label_add),
    path("label/delete/", label_collection.label_delete),
    path("label/search/", label_collection.search_by_label),
    path("label/search/search/", label_collection.search_search, name="search_search"),
    # title manage
    path("title/list/", title_manage.title_list),
    path("title/add/", title_manage.title_add),
    path("title/delete/", title_manage.title_delete),
    path("title/<int:nid>/edit/", title_manage.title_edit),
    
    #word manage
    path('word/list/', word_manage.word_list),
    path('word/add/', word_manage.word_add),
    path("word/delete/", word_manage.word_delete),
    path('word/<int:nid>/edit/', word_manage.word_edit),
    
    #conversation manage
    path("conversation/list/", views.conversation_list),

    #chatbot manage
    path('chatbot/', views.chatbot_view, name='chatbot'),

    
    
]
