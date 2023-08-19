from django.urls import path
from . views import *


urlpatterns = [
    path('', dashboard, name="index"),
    path('create-order/', createOrder, name="create_order"),
    path('update-order/<int:id>/', updateOrder, name="update_order"),
    path('delete-order/<int:id>/', deleteOrder, name="delete_order"),
    path('register/', registerPage, name="register"),
    path('login/', login, name="login"),
    path('login_process/', loginProcess, name="login_process"),
    path('logout/', logoutProcess, name="logout"),
]
