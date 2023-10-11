import datetime

from django.shortcuts import render, redirect

from todo_app.accounts.models import Account
from todo_app.tasks.forms import TaskAddForm
from todo_app.tasks.models import Task


def show_all_tasks(request):
    current_username = request.user.username
    current_account = Account.objects.get(username=current_username)
    tasks = current_account.task_set.filter(moved_to_completed=False).order_by('id')
    has_completed_tasks = current_account.task_set.filter(moved_to_completed=True).count() > 0

    current_date = datetime.date.today()

    return render(request,
                  'tasks/tasks-catalogue.html',
                  {
                      'tasks': tasks,
                      'has_completed_tasks': has_completed_tasks,
                      'current_date': current_date
                        })


def show_completed_tasks(request):
    current_account = Account.objects.get(username=request.user.username)
    completed_tasks = current_account.task_set.filter(moved_to_completed=True)

    if request.method == 'POST':
        completed_tasks.delete()

    return render(request,
                  'tasks/tasks-completed.html',
                  {'completed_tasks': completed_tasks})


def add_task(request):
    if request.method == "POST":
        form = TaskAddForm(request.POST)
        if form.is_valid():
            current_username = request.user.username
            current_account = Account.objects.get(username=current_username)

            new_task = form.save(commit=False)
            new_task.save()
            current_account.task_set.add(new_task)
            return redirect('tasks:catalogue')
    else:
        form = TaskAddForm()

    return render(request,
                  'tasks/task-add.html',
                  {'form': form})


def details_task(request, pk):
    current_task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:
            current_task.delete()
            return redirect('tasks:catalogue')
        elif 'done' in request.POST:
            current_task.is_done = True
            current_task.date_of_completion = datetime.date.today()
            current_task.save()
            return redirect('tasks:catalogue')
        elif 'move' in request.POST:
            current_task.moved_to_completed = True
            current_task.save()
            return redirect('tasks:completed-tasks')

    return render(request,
                  'tasks/task-details.html',
                  {'task': current_task})
