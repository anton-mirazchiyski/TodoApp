import datetime


def find(tasks):
    try:
        min_time = min([t.time for t in tasks if not t.is_done])
        for task in tasks:
            if task.time == min_time:
                return task
    except ValueError:
        min_time = None


def find_next_task(tasks):
    today_tasks = [t for t in tasks if t.due_date == datetime.date.today()]
    if today_tasks:
        if find(today_tasks) is not None:
            task = find(today_tasks)
            return task

    upcoming_tasks = [t for t in tasks if t.due_date > datetime.date.today()]
    if upcoming_tasks:
        return find(upcoming_tasks)


def move_done_tasks_to_completed(tasks):
    for task in tasks:
        if task.is_done:
            task.moved_to_completed = True
            task.save()


def place_completed_tasks_by_dates(tasks):
    tasks_with_dates = {}

    for task in tasks:
        if task.due_date not in tasks_with_dates:
            tasks_with_dates[task.due_date] = []
        tasks_with_dates[task.due_date].append(task)

    return tasks_with_dates


def disable_fields_if_task_done(task, form):
    if task.is_done:
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
