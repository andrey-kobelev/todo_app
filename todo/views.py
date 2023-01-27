from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login


def signup_user(request):

    context = dict()
    context['form'] = UserCreationForm

    if request.method == 'GET':
        return render(request, 'todo/sign_up.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'])

                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                context['error'] = ('That username has already been taken. '
                                    'Please choose a new username.')

                return render(request, 'todo/sign_up.html', context)
        else:
            context['error'] = 'Passwords did not match'
            return render(request, 'todo/sign_up.html', context)


def currenttodos(request):
    return render(request, 'todo/current.html')
