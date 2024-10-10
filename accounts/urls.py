from django.urls import path
from .views import CreateAccountView, AccountDetailView, DepositView, WithdrawView, TransferView, TransactionHistoryView

urlpatterns = [
    path('accounts/', CreateAccountView.as_view(), name='create_account'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction_history'),
]