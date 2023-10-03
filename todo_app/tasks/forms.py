from django import forms

from todo_app.tasks.models import Task


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date']

        labels = {
                'name': 'What',
                'due_date': 'When',
                'description': 'Describe',
                 }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control-lg',
                    # 'style': 'height: 100%',
                    'placeholder': 'Name'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control-lg',
                    'style': 'height: 100%; width: 80%',
                    'placeholder': 'Description'
                }
            ),
            'due_date': forms.DateInput(
                attrs={
                    'class': 'form-control-lg',
                    'placeholder': 'Ex: 2023-09-22'
                }
            )
        }

