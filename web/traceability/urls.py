from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('keys/active/', views.ActiveKeysList.as_view(), name='keys'),
    path('keys/inactive/', views.InactiveKeysList.as_view(), name='keys_inactive'),
    path('keys/new/', views.PendingKeysList.as_view(), name='keys_new'),
]