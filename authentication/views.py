from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrarPersonalSerializer, LoginSerializer, RegistrarAlunoSerializer, AlterarSenhaSerializer


class RegistrarPersonalView(APIView):

    @swagger_auto_schema(request_body=RegistrarPersonalSerializer)
    def post(self, request):
        serializer = RegistrarPersonalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Personal Trainer registrado com sucesso."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegistrarAlunoView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RegistrarAlunoSerializer)
    def post(self, request):
        serializer = RegistrarAlunoSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Aluno registrado com sucesso."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
class AlterarSenhaView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AlterarSenhaSerializer)
    def post(self, request):
        serializer = AlterarSenhaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['nova_senha'])
        user.save()
        
        return Response({"message":"Senha alterada com sucesso."}, status=status.HTTP_200_OK)

