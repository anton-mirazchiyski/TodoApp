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
