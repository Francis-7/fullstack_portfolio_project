from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('quiz_page/<int:quiz_id>/', views.quiz_page, name='quiz_page'),
  path('quiz_list/', views.quiz_list, name='quiz_list'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('calculate_score/', views.calculate_score, name='calculate_score'),
  path('quiz', views.quiz_list_view, name='quiz'),
]