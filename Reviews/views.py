from .models import ReviewModel

# Autenticação
from .serializers import ReviewModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewView(APIView):
    @swagger_auto_schema(
        operation_summary="Busca uma review específica",
        responses={
            200: ReviewModelSerializer(),
            400: "Review com id #{id_arg} não existe"
        }
    )
    def get(self, request, id_arg):
        queryset = self.singleReview(id_arg)

        if queryset:
            serializer = ReviewModelSerializer(queryset)

            return Response(serializer.data)
        else:
            return Response({ 'msg': f'Review com id #{id_arg} não existe'}, status=status.HTTP_400_BAD_REQUEST)
        
    def singleReview(self, id_arg):
        try:
            queryset = ReviewModel.objects.get(id=id_arg)
            return queryset
        except ReviewModel.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Cria uma nova review",
        request_body=ReviewModelSerializer,
        responses={
            201: ReviewModelSerializer(),
            400: "Bad Request"
        })
    def post(self, request):
        serializer = ReviewModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_summary="Atualiza uma review existente",
        request_body=ReviewModelSerializer,
        responses={
            200: ReviewModelSerializer(),
            400: "Bad Request",
            404: "Not Found"
        })
    def put(self, request, id_arg):
        review = self.singleReview(id_arg)
        serializer = ReviewModelSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Deleta uma review",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description="Lista de IDs das reviews a serem deletadas."
        ),
        responses={
            204: "No Content",
            404: "item [id] não encontrado"
        })
    def delete(self, request):
        id_erro = ""
        erro = False
        for id in request.data:
            review = ReviewModel.objects.get(id=id)
        if review:
            review.delete()
        else:
            id_erro += str(id)
            erro = True
        if erro:
            return Response({'error': f'item [{id_erro}] não encontrado'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
