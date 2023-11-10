import datetime

from django.shortcuts import render, redirect

from todo_app.tasks.forms import TaskAddForm, TaskEditForm
from todo_app.utils.shared_utils import get_current_account_from_username, get_current_task_from_current_account
from todo_app.utils.tasks_utils import find_next_task, find_due_date_tasks, move_done_tasks_to_completed, \
    place_completed_tasks_by_dates, task_in_the_past, disable_fields_if_task_done


def show_all_tasks(request):
    current_account = get_current_account_from_username(request)
    tasks = current_account.task_set.filter(moved_to_completed=False).order_by('id')
    has_completed_tasks = current_account.task_set.filter(moved_to_completed=True).count() > 0
    done_tasks = current_account.task_set.filter(is_done=True, moved_to_completed=False)

    next_task = find_next_task(list(tasks))
    number_of_due_date_tasks = find_due_date_tasks(list(tasks))

    context = {
        'tasks': tasks,
        'has_completed_tasks': has_completed_tasks,
        'next_task': next_task,
        'number_of_due_date_tasks': number_of_due_date_tasks,
        'number_of_tasks_done': done_tasks.count()
    }

    return render(request, 'tasks/tasks-catalogue.html', context)


def show_completed_tasks(request):
    current_account = get_current_account_from_username(request)
    completed_tasks = current_account.task_set.filter(moved_to_completed=True)

    tasks_with_dates = place_completed_tasks_by_dates(list(completed_tasks))

    if request.method == 'POST':
        completed_tasks.delete()
        tasks_with_dates.clear()

    context = {
        'completed_tasks': completed_tasks,
        'tasks_with_dates': tasks_with_dates
    }

    return render(request, 'tasks/tasks-completed.html', context)


def add_task(request):
    if request.method == "POST":
        form = TaskAddForm(request.POST)
        if form.is_valid():
            current_account = get_current_account_from_username(request)
            new_task = form.save(commit=False)
            new_task.save()
            current_account.task_set.add(new_task)
            return redirect('tasks:catalogue')
    else:
        form = TaskAddForm()

    return render(request, 'tasks/task-add.html', {'form': form})


def details_task(request, pk):
    current_account = get_current_account_from_username(request)
    current_task = current_account.task_set.get(pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:
            current_task.delete()
            return redirect('tasks:catalogue')

    context = {
        'task': current_task,
        'task_in_the_past': task_in_the_past(current_task)
    }
    return render(request, 'tasks/task-details.html', context)


def edit_task(request, pk):
    current_account = get_current_account_from_username(request)
    task_to_edit = current_account.task_set.get(pk=pk)

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task_to_edit)
        if form.is_valid():
            form.save()
            return redirect('tasks:details-task', pk=pk)
    else:
        form = TaskEditForm(instance=task_to_edit)
        disable_fields_if_task_done(task_to_edit, form)

    context = {
        'form': form,
        'task': task_to_edit,
    }
    return render(request, 'tasks/task-edit.html', context)


def complete_task_functionality(request, pk):
    current_task = get_current_task_from_current_account(request, pk)
    current_task.is_done = True
    current_task.date_of_completion = datetime.date.today()
    current_task.save()
    return redirect('tasks:catalogue')


def move_all_done_tasks(request):
    current_account = get_current_account_from_username(request)
    done_tasks = current_account.task_set.filter(is_done=True, moved_to_completed=False)
    if done_tasks:
        move_done_tasks_to_completed(done_tasks)
        return redirect(request.META['HTTP_REFERER'])


def move_current_done_task(request, pk):
    current_task = get_current_task_from_current_account(request, pk)
    current_task.moved_to_completed = True
    current_task.save()
    return redirect('tasks:catalogue')
