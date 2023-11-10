from django.contrib.auth import get_user_model


def get_current_account_from_username(request):
    UserModel = get_user_model()
    current_username = request.user.username
    current_account = UserModel.objects.get(username=current_username)
    return current_account


def get_current_task_from_current_account(request, pk):
    current_account = get_current_account_from_username(request)
    current_task = current_account.task_set.get(pk=pk)
    return current_task
