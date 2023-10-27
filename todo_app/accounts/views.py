from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from todo_app.accounts.forms import RegistrationForm, AccountLoginForm, AccountLogoutForm


UserModel = get_user_model()


def index(request):
    user = request.user

    try:
        username = user.username
        current_account = UserModel.objects.get(username=username)
        tasks = current_account.task_set.filter(moved_to_completed=False)
    except ObjectDoesNotExist:
        tasks = None

    return render(request,
                  'home-page.html',
                  {'user': user, 'tasks': tasks})


def login_account(request):
    if request.method == 'POST':
        form = AccountLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks:catalogue')
        else:
            pass
    else:
        form = AccountLoginForm()
    return render(request,
                  'accounts/account-login.html',
                  {'form': form})


def logout_account(request):
    if request.method == 'POST':
        form = AccountLogoutForm(request.POST)
        logout(request)
        return redirect('accounts:home-page')
    else:
        form = AccountLogoutForm()
    return render(request,
                  'accounts/account-logout.html',
                  {'form': form})


def create_new_account(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            repeated_password = form.cleaned_data.get('password2')

            if password == repeated_password:
                account = form.save(commit=False)
                account.save()

                user = UserModel.objects.get(username=username)
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('accounts:home-page')
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request,
                  'accounts/account-create.html',
                  {'form': form})
