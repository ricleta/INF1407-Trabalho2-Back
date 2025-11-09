from django.urls import path
from . import views

app_name = 'Reviews'

urlpatterns = [
    path('<int:id_arg>/', views.ReviewView.as_view(), name='review-detail'),
    path('', views.ReviewView.as_view(), name='review-list-create'),
    path('<int:id_arg>/', views.ReviewView.as_view(), name='review-update'),
    path('', views.ReviewView.as_view(), name='review-delete'),
]