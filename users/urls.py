from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.Register.as_view(), name = 'register user'),
    path('token/', views.Token.as_view(), name = 'generate token')
]
