
from django.urls import path

from .views import RegistrarPersonalView, LoginView, RegistrarAlunoView, AlterarSenhaView

urlpatterns = [
    path('personal/register/', RegistrarPersonalView.as_view()),
    path('aluno/register/', RegistrarAlunoView.as_view()),
    path('login/', LoginView.as_view()),
    path('alterar-senha/', AlterarSenhaView.as_view()),

]
