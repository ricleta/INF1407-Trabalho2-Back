from .models import GamesModel

# Autenticação
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import GamesModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GamesView(APIView):
    '''
    View to handle CRUD operations for GamesModel.
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def singleGame(self, id_arg):
        '''
        Helper method to get a single game by ID.
        '''
        try:
            queryset = GamesModel.objects.get(id=id_arg)
            return queryset
        except GamesModel.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Busca todos os jogos ou um jogo específico",
        responses={
            200: GamesModelSerializer(many=True),
            404: "Game not found"
        }
    )
    def get(self, request, id_arg=None):
        '''
        Get all games or a specific game by ID.
        '''
        if id_arg:
            # Get a single game by ID
            try:
                queryset = GamesModel.objects.get(id=id_arg)
                serializer = GamesModelSerializer(queryset)
                return Response(serializer.data)
            except GamesModel.DoesNotExist:
                return Response({'msg': f'Game with id #{id_arg} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all games
            queryset = GamesModel.objects.all()
            serializer = GamesModelSerializer(queryset, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Cria um novo jogo",
        request_body=GamesModelSerializer,
        security=[{'Token': []}],
        responses={
            201: GamesModelSerializer(),
            400: "Bad Request"
        })
    def post(self, request):
        '''
        Create a new game.
        '''
        serializer = GamesModelSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming the developer is the authenticated user
            serializer.save(developer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Atualiza um jogo existente",
        request_body=GamesModelSerializer,
        security=[{'Token': []}],
        responses={
            200: GamesModelSerializer(),
            400: "Bad Request",
            404: "Not Found"
        })
    def put(self, request, id_arg):
        '''
        Update an existing game.
        '''
        game = self.singleGame(id_arg)
        if not game:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GamesModelSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Deleta um jogo",
        security=[{'Token': []}],
        responses={
            204: "No Content",
            404: "Not Found"
        })
    def delete(self, request, id_arg):
        '''
        Delete a game.
        '''
        game = self.singleGame(id_arg)
        if game:
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': f'item [{id_arg}] não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class MyGamesView(APIView):
    """
    View to list games created by the currently authenticated user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Busca os jogos do usuário autenticado",
        security=[{'Token': []}],
        responses={
            200: GamesModelSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        '''
        Get games created by the authenticated user.
        '''
        queryset = GamesModel.objects.filter(developer=request.user)
        serializer = GamesModelSerializer(queryset, many=True)
        return Response(serializer.data)
