from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms

from todo_app.tasks.models import Task


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'time']

        labels = {
                'name': 'What',
                'due_date': 'When',
                'description': 'Description',
                'time': 'At'
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
                    'style': 'height: 50%; width: 80%',
                    'placeholder': 'Description'
                }
            ),
            'due_date': DatePickerInput(
                options={
                    'format': "MM-DD-YYYY"
                },
                attrs={
                    'class': 'form-control-lg',
                    'style': 'width: 50%',
                    'placeholder': 'Date'
                }
            ),
            'time': TimePickerInput(
                options={
                    'format': 'HH:mm'
                },
                attrs={
                    'class': 'form-control-lg',
                    'style': 'width: 50%',
                    'placeholder': 'Time'
                }
            )
        }


class TaskEditForm(TaskAddForm):
    pass
