#from django.shortcuts import render
#from django.views.generic import ListView, CreateView
#from django.views.generic.edit import UpdateView, DeleteView
#from django.urls import reverse_lazy, reverse

#from .forms import ReviewForm
#from django.contrib.auth.models import Group

#from django.http import HttpResponseRedirect
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm

from .models import ReviewModel

# Autenticação
from .serializers import ReviewModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewView(APIView):
    def get(self, request, id_arg):
        queryset = self.singleReview(id_arg)
        if queryset:
            serializer = ReviewModelSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({ 'msg': f'Review com id #{id_arg} não existe'}, status.HTTP_400_BAD_REQUEST)
        
    def singleReview(self, id_arg):
        try:
            queryset = ReviewModel.objects.get(id=id_arg)
            return queryset
        except ReviewModel.DoesNotExist:
            return None

    def post(self, request):
        serializer = ReviewModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id_arg):
        review = self.singleReview(id_arg)
        serializer = ReviewModelSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id_erro = ""
        erro = False
        for id in request.data:
            review = ReviewModel.objects.get(id=id)
        if review:
            review.delete()
        else:
            id_erro += str(id)
            erro = True
        if erro:
            return Response({'error': f'item [{id_erro}] não encontrado'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
