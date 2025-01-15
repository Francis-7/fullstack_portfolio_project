from rest_framework_simplejwt import views as jwt_views
from django.urls import path

urlpatterns = [
  path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]