from django.conf import settings
from django.contrib.auth import authenticate,login, logout
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.
def dashboard(request):
    order = Order.objects.all()
    total_orders = order.count()
    orders_delivered = Order.objects.filter(status='Delivered').count()
    pending_delivered = Order.objects.filter(status='Pending').count()
    context = {'order': order, 'total_orders': total_orders, 'pending_delivered': pending_delivered,
               'orders_delivered': orders_delivered}
    return render(request, 'dashboard.html', context)


def createOrder(request):
    action = 'create'
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            template = render_to_string('email_template.html', {'name': request.user})
            email = EmailMessage(
                'Transactional Email',
                template,
                settings.Email_Host_user,
                [request.user.email],
            )
            email.fail_silently = False
            email.send()
    context = {'action': action, 'form': form}
    return render(request, 'order_form.html', context)


def updateOrder(request, id):
    action = 'update'
    product = Order.objects.get(id=id)
    form = OrderForm(instance=product)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Order has been updated successfully")
            return redirect('/')
    context = {'action': action, 'form': form, 'product': product}
    return render(request, 'order_form.html', context)

def deleteOrder(request, id):
    action = 'delete'
    product = Order.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    context = {'action': action, 'product': product}
    return render(request, 'order_form.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)

                return redirect('/')


        context = {'form':form}
        return render(request, 'signup.html', context)


def login(request):
    return render(request, 'login.html', )


def loginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get('password')
    print(username)
    print(password)

    user = authenticate(request=request, username =username,password=password)
    if user is not None:
        login(request=request, user=user)
        messages.success(request, "Login! Successfull")
        return redirect("/")
    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return redirect("login")


def logoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("login")
