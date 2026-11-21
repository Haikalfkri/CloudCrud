import logging

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)

@extend_schema(methods=["GET"], responses=ProductSerializer(many=True))
@extend_schema(methods=["POST"], request=ProductSerializer, responses={201: ProductSerializer})
@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(Product.objects.all(), request)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    logger.info("Product created: %s", product.id)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(methods=["GET"], responses=ProductSerializer)
@extend_schema(methods=["PUT"], request=ProductSerializer, responses=ProductSerializer)
@extend_schema(methods=["DELETE"], responses={204: None})
@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        return Response(ProductSerializer(product).data)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Product updated: %s", product.id)
        return Response(serializer.data)

    # DELETE
    product.delete()
    logger.info("Product deleted: %s", pk)
    return Response(status=status.HTTP_204_NO_CONTENT)