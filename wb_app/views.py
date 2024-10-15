from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import fetch_product_info
from .models import Product
from .serializers import ProductSerializer

class FetchProductInfo(APIView):
    def post(self, request):
        article = request.data.get('article')
        print(request.data)
        if not article:
            return Response({"error": "Article is required"}, status=status.HTTP_400_BAD_REQUEST)
        fetch_product_info.delay(article)
        return Response({"message": "Task started"}, status=status.HTTP_202_ACCEPTED)

class ListProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

