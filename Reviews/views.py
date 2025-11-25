from .models import ReviewModel

# Autenticação
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ReviewModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewView(APIView):
    '''
    View to handle CRUD operations for ReviewModel.
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Busca reviews",
        operation_description="Busca uma review específica por ID, ou filtra reviews por jogo ou pelo usuário autenticado. Se nenhum filtro for fornecido, retorna todas as reviews.",
        manual_parameters=[
            openapi.Parameter('game_id', openapi.IN_QUERY, description="ID do jogo para filtrar as reviews", type=openapi.TYPE_INTEGER),
            openapi.Parameter('my_reviews', openapi.IN_QUERY, description="Retorna apenas as reviews do usuário autenticado", type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            200: ReviewModelSerializer(many=True),
            404: "Review not found"
        }
    )
    def get(self, request, id_arg=None):
        '''
        Handles GET requests to retrieve reviews.
        '''
        if id_arg:
            # Busca uma review específica pelo ID na URL
            queryset = self.singleReview(id_arg)
            if queryset:
                serializer = ReviewModelSerializer(queryset)
                return Response(serializer.data)
            else:
                return Response({ 'msg': f'Review com id #{id_arg} não existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Filtra reviews com base nos query parameters
            queryset = ReviewModel.objects.all()
            game_id = request.query_params.get('game_id')
            my_reviews = request.query_params.get('my_reviews')

            if game_id:
                queryset = queryset.filter(game__id=game_id)

            if my_reviews and str(my_reviews).lower() in ['true', '1']:
                if request.user.is_authenticated:
                    queryset = queryset.filter(user=request.user)
                else:
                    # Retorna uma lista vazia se 'my_reviews' for solicitado sem autenticação
                    queryset = ReviewModel.objects.none()

            serializer = ReviewModelSerializer(queryset, many=True)
            return Response(serializer.data)

    def singleReview(self, id_arg):
        '''
        Helper method to get a single review by ID.
        '''
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
        '''
        Handles POST requests to create a new review.
        '''
        serializer = ReviewModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
        '''
        Handles PUT requests to update an existing review.
        '''
        review = self.singleReview(id_arg)
        serializer = ReviewModelSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Deleta uma review",
        security=[{'Token': []}],
        responses={
            204: "No Content",
            404: "Review [id] não encontrado"
        })
    def delete(self, request, id_arg):
        '''
        Handles DELETE requests to remove a review.
        '''
        review = self.singleReview(id_arg)
        if review:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': f'Review [{id_arg}] não encontrado'}, status=status.HTTP_404_NOT_FOUND)
