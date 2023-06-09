from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from .models import Category, Payment
from .serializers import CategorySerializer, PaymentSerializer, Joined


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PaymentAPIListCreate(APIView):
    queryset = Category.objects.all()
    serializer


class PaymentAPIViewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
