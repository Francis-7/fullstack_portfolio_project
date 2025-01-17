from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import views
from django.urls import path
from . import views

urlpatterns = [
  path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
  path('api/questions/', views.QuestionListView.as_view(), name='question-list'),
  path('questions/', views.QuestionList.as_view(), name='question-list'),
  path('quizzes/', views.QuizList.as_view(), name='quiz-list'),
  path('home/', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('quiz_page/', views.quiz_page, name='quiz_page'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('calculate_score/', views.calculate_score, name='calculate_score'),
]