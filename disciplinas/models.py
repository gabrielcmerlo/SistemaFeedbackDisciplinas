from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome
    
    def media_notas(self):
        total = 0
        count = 0
        for feedback in self.feedback_set.all():
            total += feedback.nota
            count += 1
        return total / count if count > 0 else 0

class Feedback(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('disciplina', 'aluno')  # Impede múltiplas avaliações
    
    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.nome} - {self.nota}"