from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django import forms

class SignUpForm(UserCreationForm):
    """
    A custom user creation form that includes an email field and a group selection.
    """
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Insira um endereço de e-mail válido.')

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Tipo de Conta"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)