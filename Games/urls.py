from django.urls import path
from . import views

app_name = 'Games'

urlpatterns = [
    path('<int:id_arg>/', views.GamesView.as_view(), name='game-detail'),
    path('', views.GamesView.as_view(), name='game-list-create'),
    path('<int:id_arg>/', views.GamesView.as_view(), name='game-update'),
    path('', views.GamesView.as_view(), name='game-delete'),
]
