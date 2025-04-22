from django.contrib import admin
from django.urls import path
from disciplinas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lista_disciplinas, name='lista_disciplinas'),
    path('disciplinas/<int:disciplina_id>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('disciplinas/<int:disciplina_id>/avaliar/', views.avaliar_disciplina, name='avaliar_disciplina'),
    path('feedback/<int:feedback_id>/editar/', views.editar_feedback, name='editar_feedback'),
    path('feedback/<int:feedback_id>/excluir/', views.excluir_feedback, name='excluir_feedback'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]