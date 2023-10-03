from django.contrib import admin

from todo_app.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
