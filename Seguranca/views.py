from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.conf import settings

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
                description='User data',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'groups': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    },
                ),
            ),
            status.HTTP_404_NOT_FOUND: "User not found or not authenticated. Returns 'visitante'."
        },

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

            user_data = {
                'id': user.id,
                'username': user.username,
                'groups': list(user.groups.values('name')) # Fetches group names
            }

            return Response(user_data, status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response(
            {'username': 'visitante'},
            status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1] # token
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            oldPassword = request.data.get('old_password')
            newPassword = request.data.get('new_password1')
            confirmPassword = request.data.get('new_password2')
          
            if newPassword != confirmPassword:
                return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
          
            # Verificar se a senha atual está correta
            if user.check_password(oldPassword):
                # Alterar a senha e atualizar o token
                user.set_password(newPassword)
                user.save()
                # Atualizar token
                token, _ = Token.objects.get_or_create(user=user)
                token.delete()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, "message": "Senha alterada com sucesso."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"old_password": ["Senha atual incorreta."]}, status=status.HTTP_400_BAD_REQUEST)
            
        except (Token.DoesNotExist, AttributeError, IndexError):
            return Response({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)

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

class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        operation_summary='Reset user password',
        operation_description="Generates a temporary password for a user based on their email and returns it.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="The user's email address."),
            },
            required=['email'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Temporary password generated successfully.',
            ),
            status.HTTP_400_BAD_REQUEST: 'Email not provided.',
            status.HTTP_404_NOT_FOUND: 'User with the given email not found.',
        },
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        temporary_password = User.objects.make_random_password(length=10)
        user.set_password(temporary_password)
        user.save()

        # Send email with the temporary password
        subject = 'Your New Temporary Password'
        message = f'Your temporary password is: {temporary_password}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        return Response(
            {'message': 'A temporary password has been sent to your email address.'},
            status=status.HTTP_200_OK
        )