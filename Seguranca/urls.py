from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse_lazy

app_name = 'Seguranca'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('actual-logout/', views.actual_logout_view.as_view(), name='actual-logout'),
    path('account/password_change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('account/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
            template_name='Seguranca/password_reset_form.html',
            success_url=reverse_lazy('Seguranca:password_reset_done'),
            html_email_template_name='Seguranca/password_reset_email.html',
            subject_template_name='Seguranca/password_reset_subject.txt',
            from_email='no-reply@avaliacoes.jogos.com',
        ),
        name='password_reset'
    ),
    path('password_reset/done/', PasswordResetDoneView.as_view(
            template_name='Seguranca/password_reset_done.html',
        ),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='Seguranca/password_reset_confirm.html',
            success_url=reverse_lazy('Seguranca:password_reset_complete'),
        ),
        name='password_reset_confirm'
    ),
    path('reset/done/', views.PasswordResetComplete.as_view(
            template_name='Seguranca/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'),
    # path('user-detail/', views.UserDetailView.as_view(), name='user-detail'),
    
]