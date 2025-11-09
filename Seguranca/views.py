from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetCompleteView

from .forms import SignUpForm

from rest_framework.authtoken.views import ObtainAuthToken
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
                        
def signup(request):
    """
    Handles user registration.

    Allows a new user to register and assigns them to a specific group (GameDev or Reviewers).
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data.get('group')
            user.groups.add(group)
            return HttpResponseRedirect(reverse_lazy('home-page'))
    else:
        form = SignUpForm()
    return render(request, 'Seguranca/signup.html', {'form': form})

class login_view(LoginView):
    """
    Handles user login.

    Uses Django's built-in LoginView for authentication.
    """
    template_name = 'Seguranca/login.html'
    redirect_authenticated_user = True

@login_required
def logout_view(request):
    """
    Displays a confirmation page before logging out.
    """
    return render(request, 'Seguranca/logout.html')

class actual_logout_view(LogoutView):
    """
    Handles the actual user logout.

    Redirects the user to the home page after logging out.
    """
    def get_success_url(self):
        """
        Specifies the URL to redirect to after a successful logout.
        """
        return reverse_lazy('home-page')

class ChangePasswordView(PasswordChangeView):
    '''
    View for changing the user's password.
    '''
    template_name = 'Seguranca/change_password.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDoneView(PasswordChangeDoneView):
    '''
    View displayed after a successful password change.
    '''
    template_name = 'Seguranca/password_change_done.html'
    success_url = reverse_lazy('home-page')

class PasswordResetComplete(PasswordResetCompleteView):
    '''
    View displayed after a successful password reset.
    '''
    template_name = 'Seguranca/password_reset_complete.html'
    success_url = reverse_lazy('home-page')
