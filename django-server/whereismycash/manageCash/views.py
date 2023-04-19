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
    def get(self, request):
        query = Payment.objects.select_related("Category")
        return Response(PaymentSerializer(instance=query, many=True).data)


class PaymentAPIViewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
