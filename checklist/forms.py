from django import forms
from .models import Checklist

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = '__all__'

