from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import views
from django.urls import path
from . import views

urlpatterns = [
  path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
  path('api/questions/', views.QuestionListView.as_view(), name='question-list'),
  path('questions/', views.QuestionList.as_view(), name='question-list'),
  path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
]