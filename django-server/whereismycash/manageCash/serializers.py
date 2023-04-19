from rest_framework import serializers
from rest_framework.response import Response

from .models import Category, Payment, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    Category = CategorySerializer()
    # Owner = UserSerializer()
    class Meta:
        model = Payment
        fields = '__all__'

class Joined(serializers.Serializer):
    pass



'''class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('Category_ID', 'Category_Name', 'Payment_Type')'''
