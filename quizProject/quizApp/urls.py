from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  path('home/', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('quiz_page/<int:id>/', views.quiz_page, name='quiz_page'),
  path('quiz_list/', views.quiz_list, name='quiz_list'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('quiz_list_view/', views.quiz_list_view, name='quiz'),
  path('quiz/<int:id>/', views.quiz_detail_view, name='quiz-detail'),
  path('quiz_questions/', views.quiz_questions, name='quiz-questions'),
  path('submit_quiz/<int:id>/', views.submit_quiz, name='submit_quiz'),
  path('quiz_result/<int:id>/', views.quiz_result, name='quiz_result'),
  path('quiz/<int:id>/start/', views.start_quiz, name='start_quiz'),
  path('reset_data/', views.reset_data, name='reset_data'),
  path('add_quiz', views.add_quiz, name='add_quiz'),
  path('add_question', views.add_question, name='add_question'),
  path('add_choice', views.add_choice, name='add_choice'),

]

urlpatterns = format_suffix_patterns(urlpatterns)