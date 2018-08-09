from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('keys/', views.KeysList.as_view(), name='keys'),
]