import datetime

from django.core.exceptions import ValidationError


def validate_date_is_not_in_the_past(date):
    if date < datetime.date.today():
        raise ValidationError('The date cannot be in the past!')
