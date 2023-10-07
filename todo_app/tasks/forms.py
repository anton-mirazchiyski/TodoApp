from bootstrap_datepicker_plus.widgets import DatePickerInput
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
                    'placeholder': 'Name'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control-lg',
                    'style': 'height: 50%; width: 60%',
                    'placeholder': 'Description'
                }
            ),
            'due_date': DatePickerInput(
                options={
                    'format': "MM/DD/YYYY"
                },
                attrs={
                    'class': 'form-control-lg',
                    'style': 'width: 35%'
                }
            )
        }
