from rest_framework import serializers
from .models import Expenses

class ExpensesSerializer(serializers.ModelSerializer):


    class Meta:
        model=Expenses
        fields=['date', 'description', 'amount', 'category' ]