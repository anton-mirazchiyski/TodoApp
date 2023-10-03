from django.contrib import admin

from todo_app.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
