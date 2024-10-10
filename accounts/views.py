from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, CreateAccountSerializer
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal, InvalidOperation

class CreateAccountView(generics.CreateAPIView):
    serializer_class = CreateAccountSerializer

    def perform_create(self, serializer):
        account = serializer.save()
        user = account.user
        user.set_password(self.request.data['user']['password'])
        user.save()

class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

class DepositView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        print(f"Attempting deposit for user: {user.username}")  # Debug print

        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            print(f"No account found for user: {user.username}")  # Debug print
            return Response({'error': f'No account found for user {user.username}'}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount')
        print(f"Deposit amount: {amount}")  # Debug print
        
        try:
            amount = Decimal(amount)
        except (InvalidOperation, TypeError, ValueError):
            return Response({'error': f'Invalid amount: {amount}'}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= Decimal('0'):
            return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance += amount
            account.save()

            transaction_obj = Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='deposit'
            )

        serializer = self.get_serializer(transaction_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WithdrawView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        print(f"Attempting withdrawal for user: {user.username}")  # Debug print

        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            print(f"No account found for user: {user.username}")  # Debug print
            return Response({'error': f'No account found for user {user.username}'}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount')
        print(f"Withdrawal amount: {amount}")  # Debug print
        
        try:
            amount = Decimal(amount)
        except (InvalidOperation, TypeError, ValueError):
            return Response({'error': f'Invalid amount: {amount}'}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= Decimal('0'):
            return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        if account.balance < amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance -= amount
            account.save()

            transaction_obj = Transaction.objects.create(
                account=account,
                amount=-amount,  # Negative amount for withdrawal
                transaction_type='withdraw'
            )

        serializer = self.get_serializer(transaction_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransferView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        from_account = request.user.account
        to_account_id = request.data.get('to_account')
        amount = request.data.get('amount')

        try:
            to_account = Account.objects.get(id=to_account_id)
        except Account.DoesNotExist:
            return Response({'error': f'Recipient account with ID {to_account_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            amount = Decimal(amount).quantize(Decimal('.01'))
        except (InvalidOperation, TypeError, ValueError):
            return Response({'error': f'Invalid amount: {amount}. Please provide a valid number.'}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= Decimal('0'):
            return Response({'error': 'Transfer amount must be positive.'}, status=status.HTTP_400_BAD_REQUEST)

        if amount < Decimal('0.01'):
            return Response({'error': 'Minimum transfer amount is 0.01.'}, status=status.HTTP_400_BAD_REQUEST)

        if from_account.balance < amount:
            return Response({'error': 'Insufficient funds for this transfer.'}, status=status.HTTP_400_BAD_REQUEST)

        if from_account == to_account:
            return Response({'error': 'Cannot transfer to the same account.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                from_account.balance -= amount
                from_account.save()

                to_account.balance += amount
                to_account.save()

                from_transaction = Transaction.objects.create(
                    account=from_account,
                    amount=-amount,
                    transaction_type='transfer_out',
                    description=f"Transfer to {to_account.user.username} (Account: {to_account.id})"
                )

                to_transaction = Transaction.objects.create(
                    account=to_account,
                    amount=amount,
                    transaction_type='transfer_in',
                    description=f"Transfer from {from_account.user.username} (Account: {from_account.id})"
                )

            serializer = self.get_serializer(from_transaction)
            return Response({
                'message': 'Transfer successful',
                'transaction': serializer.data,
                'from_account': f"{from_account.user.username} (ID: {from_account.id})",
                'to_account': f"{to_account.user.username} (ID: {to_account.id})",
                'amount': str(amount)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': 'An unexpected error occurred during the transfer. Please try again later or contact support.',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account).order_by('-timestamp')