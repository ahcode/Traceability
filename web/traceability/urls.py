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
    path('key/modify/<slug:hash>', views.ModifyKey.as_view(), name='modify_key'),
    path('key/search/', views.KeySearch, name='key_search'),
    path('transactions/', views.TransactionsList.as_view(), name='transactions'),
    path('transactions/<slug:hash>', views.TransactionDetail.as_view(), name='transaction_details'),
    path('remote_register/<slug:value>', views.ChangeRemoteRegisterStatus, name='remote_register'),
    path('ids/search/', views.IdSearch.as_view(), name='id_search'),
    path('ids/details/<slug:id>', views.IdDetails.as_view(), name='id_details'),
]