from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['nota', 'comentario']
    
    def clean_nota(self):
        nota = self.cleaned_data['nota']
        if nota < 1 or nota > 5:
            raise forms.ValidationError("A nota deve estar entre 1 e 5.")
        return nota