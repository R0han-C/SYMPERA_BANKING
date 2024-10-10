from rest_framework import serializers
from .models import User, Account, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth']
        extra_kwargs = {'password': {'write_only': True}}

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_number', 'balance', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'transaction_type', 'timestamp', 'description']

class CreateAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    initial_balance = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Account
        fields = ['user', 'initial_balance', 'account_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        account = Account.objects.create(user=user, balance=validated_data['initial_balance'], account_number=validated_data['account_number'])
        return account