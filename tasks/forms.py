from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
            'labels': forms.SelectMultiple(attrs={'size': 5}),
        }