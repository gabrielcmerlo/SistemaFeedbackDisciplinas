from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Disciplina, Feedback
from .forms import FeedbackForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_disciplinas')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        disciplina.media = disciplina.media_notas()
    return render(request, 'lista_disciplinas.html', {'disciplinas': disciplinas})

@login_required
def detalhes_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    feedbacks = Feedback.objects.filter(disciplina=disciplina)
    user_feedback = Feedback.objects.filter(disciplina=disciplina, aluno=request.user).first()
    
    return render(request, 'detalhes_disciplina.html', {
        'disciplina': disciplina,
        'feedbacks': feedbacks,
        'user_feedback': user_feedback,
        'media': disciplina.media_notas(),
    })

@login_required
def avaliar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    # Verifica se o usuário já avaliou
    if Feedback.objects.filter(disciplina=disciplina, aluno=request.user).exists():
        return redirect('detalhes_disciplina', disciplina_id=disciplina.id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.disciplina = disciplina
            feedback.aluno = request.user
            feedback.save()
            return redirect('detalhes_disciplina', disciplina_id=disciplina.id)
    else:
        form = FeedbackForm()
    
    return render(request, 'avaliar_disciplina.html', {
        'form': form,
        'disciplina': disciplina,
    })

@login_required
def editar_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, aluno=request.user)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('detalhes_disciplina', disciplina_id=feedback.disciplina.id)
    else:
        form = FeedbackForm(instance=feedback)
    
    return render(request, 'editar_feedback.html', {
        'form': form,
        'disciplina': feedback.disciplina,
    })

@login_required
def excluir_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, aluno=request.user)
    disciplina_id = feedback.disciplina.id
    feedback.delete()
    return redirect('detalhes_disciplina', disciplina_id=disciplina_id)