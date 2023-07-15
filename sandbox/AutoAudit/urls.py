from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('history/', views.history, name='history'),
    path('report/<int:sample_id>/', views.report, name='report'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('search/', views.search, name='search'),

]



