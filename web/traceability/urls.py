from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('keys/active/', views.ActiveKeysList.as_view(), name='keys'),
    path('keys/inactive/', views.InactiveKeysList.as_view(), name='keys_inactive'),
    path('keys/pending/', views.PendingKeysList.as_view(), name='keys_pending'),
    path('keys/action/activate/<slug:hash>/', views.ActivateKey, name='activate_key'),
    path('keys/action/deactivate/<slug:hash>/', views.DeactivateKey, name='deactivate_key'),
    path('keys/action/remove/<slug:hash>/', views.RemoveKey, name='remove_key'),
    path('keys/details/<slug:hash>', views.KeyDetails.as_view(), name='key_details'),
    path('keys/new/', views.NewKey.as_view(), name='new_key'),
    path('key/search/', views.KeySearch, name='key_search'),
]