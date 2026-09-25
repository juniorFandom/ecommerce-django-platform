from django.urls import path
from .call_back import pawapay_callback
from .views import PaiementView

urlpatterns = [
    path('callback/', pawapay_callback, name='pawapay-callback'),
    path('list/', PaiementView.as_view(), name='paiement-list'),
    path('create/', PaiementView.as_view(), name='paiement-create'),
    path('<str:reference>/', PaiementView.as_view(), name='paiement-detail'),
    path('<str:reference>/delete/', PaiementView.as_view(), name='paiement-delete')   
]