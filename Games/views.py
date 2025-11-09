#from django.shortcuts import render
#from django.views.generic import ListView, CreateView
#from django.views.generic.edit import UpdateView, DeleteView
#from django.views.generic.detail import DetailView
#from django.urls import reverse_lazy, reverse
#from django.contrib import messages
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.http import HttpResponseRedirect
#from .models import GamesModel
#from .forms import GamesForm

from .models import GamesModel

# Autenticação
from .serializers import GamesModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GamesView(APIView):
    def get(self, request, id_arg):
        queryset = self.singleGame(id_arg)
        if queryset:
            serializer = GamesModelSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({'msg': f'Games com id #{id_arg} não existe'}, status.HTTP_400_BAD_REQUEST)
    
    def singleGame(self, id_arg):
        try:
            queryset = GamesModel.objects.get(id=id_arg)
            return queryset
        except GamesModel.DoesNotExist:
            return None
    
    def post(self, request):
        serializer = GamesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id_arg):
        game = self.singleGame(id_arg)
        serializer = GamesModelSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id_erro = ""
        erro = False
        for id in request.data:
            jogo = GamesModel.objects.get(id=id)
        if jogo:
            jogo.delete()
        else:
            id_erro += str(id)
            erro = True
        if erro:
            return Response({'error': f'item [{id_erro}] não encontrado'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)