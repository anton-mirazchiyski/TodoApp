from django.core.exceptions import ValidationError


def validate_name_contains_valid_symbols_and_numbers(name):
    for char in name:
        if not char.isalnum() and char != '_':
            raise ValidationError("Your username can only contain letters, "
                                  "numbers and underscores.")


def validate_password_is_strong(password):
    has_letter = False
    has_digit = False
    has_capital_letter = False

    for char in password:
        if char.isupper():
            has_capital_letter = True
        elif char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_digit = True

    if (not has_letter) or (not has_capital_letter) or (not has_digit):
        raise ValidationError('Password must contain at least one letter, '
                              'at least one capital letter and at least one number!')
