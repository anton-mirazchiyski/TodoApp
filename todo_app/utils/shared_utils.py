from django.contrib.auth import get_user_model


def get_current_account_from_username(request):
    UserModel = get_user_model()
    current_username = request.user.username
    current_account = UserModel.objects.get(username=current_username)
    return current_account
