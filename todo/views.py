from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')


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
                return redirect('currenttodo')
            except IntegrityError:
                context['error'] = ('That username has already been taken. '
                                    'Please choose a new username.')

                return render(request, 'todo/sign_up.html', context)
        else:
            context['error'] = 'Passwords did not match'
            return render(request, 'todo/sign_up.html', context)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponse('ERROR')


def loginuser(request):
    context = dict()
    context['form'] = AuthenticationForm
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', context)
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])

        if user is None:
            context['error'] = 'Username and Password did not match'
            return render(request, 'todo/loginuser.html', context)
        else:
            login(request, user)
            return redirect('currenttodo')


def createtodo(request):

    context = {
        'form': TodoForm
    }

    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', context)
    else:
        try:
            # соединить информацию полученную от пользователя
            # с нашей формой
            form = TodoForm(request.POST)  # TodoForm сама разберет содержимое POST запроса как надо

            # сохранить новую форму в БД создав объект newtodo
            newtodo = form.save(commit=False)

            # привязать объект newtodo к конкретному пользователю
            # указав пользователя создавшего запись
            newtodo.user = request.user

            # Сохранить объект в БД
            newtodo.save()

            # перенаправить пользователя на список записей
            return redirect('currenttodo')
        except ValueError:
            # указать в ошибке, что переданы неверные данные
            context['error'] = 'Bad data passed in'

            # вернуть снова форму с указанной ошибкой
            return render(request, 'todo/createtodo.html', context)


def currenttodos(request):
    return render(request, 'todo/current.html')
