from django.urls import path, include
from .views import index, create_new_account, login_account, logout_account

app_name = 'accounts'

urlpatterns = [
    path('', index, name='home-page'),
    path('account/', include([
        path('create/', create_new_account, name='create-account'),
        path('login/', login_account, name='login-account'),
        path('logout/', logout_account, name='logout-account')
    ]))
]
