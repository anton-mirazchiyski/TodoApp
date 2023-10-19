import datetime

from django.shortcuts import render, redirect

from todo_app.accounts.models import Account
from todo_app.tasks.forms import TaskAddForm
from todo_app.tasks.models import Task
from utils.tasks_utils import find_next_task, move_done_tasks_to_completed, place_completed_tasks_by_dates


def show_all_tasks(request):
    current_username = request.user.username
    current_account = Account.objects.get(username=current_username)
    tasks = current_account.task_set.filter(moved_to_completed=False).order_by('id')
    has_completed_tasks = current_account.task_set.filter(moved_to_completed=True).count() > 0
    done_tasks = current_account.task_set.filter(is_done=True, moved_to_completed=False)

    next_task = find_next_task(list(tasks))
    current_date = datetime.date.today()

    if request.method == 'POST':
        if 'move' in request.POST:
            move_done_tasks_to_completed(tasks)
            return redirect('tasks:catalogue')

    context = {
        'tasks': tasks,
        'has_completed_tasks': has_completed_tasks,
        'next_task': next_task,
        'current_date': current_date,
        'number_of_tasks_done': done_tasks.count()
    }

    return render(request,'tasks/tasks-catalogue.html', context)


def show_completed_tasks(request):
    current_account = Account.objects.get(username=request.user.username)
    completed_tasks = current_account.task_set.filter(moved_to_completed=True)

    tasks_with_dates = place_completed_tasks_by_dates(list(completed_tasks))

    if request.method == 'POST':
        completed_tasks.delete()

    context = {
        'completed_tasks': completed_tasks,
        'tasks_with_dates': tasks_with_dates
    }

    return render(request,'tasks/tasks-completed.html', context)


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
    current_account = Account.objects.get(username=request.user.username)
    current_task = current_account.task_set.get(pk=pk)

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
