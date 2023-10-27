from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordStrengthValidator:
    def __init__(self):
        self.has_letter = False
        self.has_digit = False
        self.has_capital_letter = False

    def check_password(self, password):
        for char in password:
            if char.isupper():
                self.has_capital_letter = True
            elif char.isalpha():
                self.has_letter = True
            elif char.isdigit():
                self.has_digit = True

    def validate(self, password, user=None):
        self.check_password(password)
        if (not self.has_letter) or (not  self.has_capital_letter) or (not self.has_digit):
            raise ValidationError(
                _("Password must contain at least one letter, "
                  "at least one capital letter and at least one number!"),
                code="password_too_short",
            )

    def get_help_text(self):
        return _(
            "Password must contain at least one letter, "
            "at least one capital letter and at least one number!"
        )
