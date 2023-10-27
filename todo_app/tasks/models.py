from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from todo_app.tasks.validators import validate_date_is_not_in_the_past


UserModel = get_user_model()


class Task(models.Model):
    MAX_LEN_NAME = 30
    MIN_LEN_NAME = 5

    name = models.CharField(max_length=MAX_LEN_NAME,
                            validators=[MinLengthValidator(MIN_LEN_NAME)],
                            null=False, blank=False)

    description = models.TextField(null=True, blank=True)

    due_date = models.DateField(validators=[validate_date_is_not_in_the_past],
                                null=False, blank=False)

    time = models.TimeField(null=True, blank=True)

    is_done = models.BooleanField(null=True, default=False)

    moved_to_completed = models.BooleanField(null=True, default=False)

    date_of_completion = models.DateField(null=True, blank=True)

    account = models.ForeignKey(UserModel,
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return f'{self.name} for {self.due_date}'
