from django.urls import path, include

from data import views

urlpatterns = [
    path('', views.StoreData.as_view(), name = 'store data'),
    path('<str:key>/', views.ManipulateData.as_view(), name = 'manipulate data')
]
