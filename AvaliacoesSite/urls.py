"""
URL configuration for AvaliacoesSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from Reviews import views as views_reviews
from rest_framework.authtoken import views as authtoken_views
from rest_framework import routers
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

schema_view = yasg_schema_view(
    openapi.Info(
        title="API de Exemplo",
        default_version='v1',
        description="Descrição da API de exemplo",
        contact=openapi.Contact(email="meslin@puc-rio.br"),
        license=openapi.License(name='GNU GPLv3'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth'),
    path('admin/', admin.site.urls),
    path('seguranca/', include('Seguranca.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('games/', include('Games.urls')),
    path('reviews/', include('Reviews.urls')),
    path('docs/',
        include_docs_urls(title='Documentação da API')),
    path('swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path('api/v1/',
        include(routers.DefaultRouter().urls)),
    path('openapi',
        get_schema_view(
        title="API para Jogos",
        description="API para obter dados dos jogos",),
        name='openapi-schema'),
]