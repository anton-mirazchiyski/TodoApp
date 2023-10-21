from django.urls import path

from todo_app.tasks.views import show_all_tasks, add_task, details_task, show_completed_tasks, edit_task

app_name = 'tasks'

urlpatterns = [
    path('', show_all_tasks, name='catalogue'),
    path('add/', add_task, name='add-task'),
    path('edit/<int:pk>/', edit_task, name='edit-task'),
    path('details/<int:pk>/', details_task, name='details-task'),
    path('finished/', show_completed_tasks, name='completed-tasks')
]
