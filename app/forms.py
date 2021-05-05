from django import forms
from .models import Case

class CaseModelForm(forms.ModelForm):
    
    class Meta:
        model = Case
        fields = '__all__'

class EventForm:
    pass
