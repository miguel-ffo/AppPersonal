from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Personal, Aluno


class RegistrarPersonalSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    nome_completo = serializers.CharField(write_only=True)
    cref = serializers.CharField(write_only=True)
    especialidade = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'nome_completo', 'cref', 'especialidade']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        nome_completo = validated_data.pop('nome_completo')

        # Extras
        cref = validated_data.pop('cref')
        especialidade = validated_data.pop('especialidade')


        partes = nome_completo.strip().split()

        first_name = partes[0]
        last_name = partes[-1] if len(partes) > 1 else ''

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            nome_completo=nome_completo,
            role='personal'
        )

        Personal.objects.create(user=user, cref=cref,especialidade=especialidade)
        return user


class RegistrarAlunoSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    nome_completo = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'nome_completo']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None or request.user.role != 'personal':
            raise serializers.ValidationError("Apenas um personal pode registrar um aluno.")

        email = validated_data.pop('email')
        password = validated_data.pop('password')
        nome_completo = validated_data.pop('nome_completo')

        partes = nome_completo.strip().split()
        first_name = partes[0]
        last_name = partes[-1] if len(partes) > 1 else ''

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            nome_completo=nome_completo,
            role='aluno'
        )

        personal = Personal.objects.get(user=request.user)

        Aluno.objects.create(user=user, personal=personal)

        return user




class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("Email ou senha inválidos.")

        if not user.is_active:
            raise AuthenticationFailed("Usuário inativo")

        refresh = RefreshToken.for_user(user)

        return  {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'nome': user.nome_completo,
                'role': user.role

            }

        }



