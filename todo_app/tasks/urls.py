from django.urls import path

from todo_app.tasks.views import (show_all_tasks, add_task, details_task, show_completed_tasks, edit_task,
                                  move_all_done_tasks, move_current_done_task, complete_task_functionality)

app_name = 'tasks'

urlpatterns = [
    path('', show_all_tasks, name='catalogue'),
    path('add/', add_task, name='add-task'),
    path('edit/<int:pk>/', edit_task, name='edit-task'),
    path('details/<int:pk>/', details_task, name='details-task'),
    path('complete/<int:pk>', complete_task_functionality, name='complete'),
    path('finished/', show_completed_tasks, name='completed-tasks'),
    path('move/<int:pk>/', move_current_done_task, name='move'),
    path('move_all_done/', move_all_done_tasks, name='move-all-done')
]
