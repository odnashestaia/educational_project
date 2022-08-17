from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import ProductSerializer, CartSerializer
from demo.models import Product


@csrf_exempt
def products(request):
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def products_detal(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)


class BearerAuth(TokenAuthentication):
    keyword = 'Bearer'


class CartList(APIView):
    authentication_classes = [BearerAuth, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart_item = request.user.basket_set.all()
        serializer = CartSerializer(cart_item, many=True)
        return Response(serializer.data)
