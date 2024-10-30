from django.contrib.auth import authenticate, alogin, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from calcApi.common.models import ApiRequest, ApiResponse


@csrf_protect
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwrd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin panel')

        elif user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('log in')

    context = {'user_authenticated': request.user.is_authenticated}

    return render(request, 'user_interface_templates/log_in_page.html', context)


@csrf_protect
@login_required
def admin_page(request):
    user_requests = ApiRequest.objects.filter(user=request.user).prefetch_related('responses').all()

    context = {
        'user_requests': user_requests,
        'user_name': request.user.username,
    }

    return render(request, 'user_interface_templates/admin_ui_page.html', context)