from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Swagger

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_summary='Obter o token de autenticação',
        operation_description='Retorna o token em caso de sucesso na autenticação ou HTTP 401',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password', ],
        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_summary='Obtém o username do usuário',
        operation_description="Retorna o username do usuário ou apenas visitante se o usuário não estiver autenticado",
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Token de autenticação no formato "token \<<i>valor do token</i>\>"',
                default='token ',
            ),
        ],
        responses={
            200: openapi.Response(
                description='Nome do usuário',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'username': openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        }
    )
    def get(self, request):
        '''
        Parâmetros: o token de acesso
        Retorna: o username ou 'visitante'
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response(
            {'username': user.username},
            status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response(
            {'username': 'visitante'},
            status=status.HTTP_404_NOT_FOUND)
                        
class UserRegistrationView(APIView):
    @swagger_auto_schema(
        operation_summary='Register a new user',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'group': openapi.Schema(type=openapi.TYPE_STRING, description="User group ('reviewer' or 'developer')"),
            },
            required=['username', 'password', 'email', 'group'],
        ),
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        group_name = request.data.get('group')

        if not all([username, password, email, group_name]):
            return Response(
                {'error': 'Please provide username, password, email, and group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if group_name not in ['reviewer', 'developer']:
            return Response({'error': "Group must be 'reviewer' or 'developer'"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email
        )

        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            # This case assumes the groups 'reviewer' and 'developer' exist.
            # You should create them in the Django admin panel.
            return Response({'error': f"Group '{group_name}' does not exist."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    """
    Logs out the user by deleting their authentication token.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='User logout',
        operation_description="Invalidates the user's authentication token and logs them out of the session.",
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                description='Authentication token in the format "Token <token_value>"',
                type=openapi.TYPE_STRING, required=True
            ),
        ],
        responses={
            status.HTTP_200_OK: 'Logout successful.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized.',
        },
    )
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)