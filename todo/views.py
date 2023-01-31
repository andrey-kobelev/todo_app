from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

@login_required
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

@login_required
def createtodo(request):

    # импортировать свою форму и добавить ее в context
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

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=True)

    context = {
        'todos': todos
    }

    return render(request, 'todo/current.html', context)

@login_required
def viewtodo(request, todo_pk):

    # найти нужную записись в базе данных по ее ключу todo_pk
    # функуию get_object_or_404 нужно импортировать
    # И еще! Что бы пользователь открывающий запись имел на нее право,
    # нужно что бы система сверяла не только ключ записи НО И ЕЕ АВТОРА -
    # user=request.user
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    context = {
        'todo': todo,
    }

    if request.method == 'GET':
        # Загрузить форму создания записи, что бы прям
        # в ней читать и редактировать записи.
        # В параметр добавить соответствующий объект
        # данные котрого нужно отобразить в форме
        form = TodoForm(instance=todo)

        # В context передать форму

        context['form'] = form

        # создать новый шаблон viewtodo.html
        return render(request, 'todo/viewtodo.html', context)
    else:
        try:
            # Что бы не возникла ошибка IntegrityError, котрая счиатет что мы пытаемся создать новый объект
            # Нужно уточнить, что мы хотим изменить уже существующий объект instance=todo
            form = TodoForm(request.POST, instance=todo)

            form.save()

            return redirect('currenttodo')
        except ValueError:
            form = TodoForm(instance=todo)
            context['error'] = 'Bad info'
            context['form'] = form

            return render(request, 'todo/viewtodo.html', context)

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodo')
    else:
        pass

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')
    else:
        pass

@login_required
def completedtodo(request):
    # указать порядок перечисления объектов(дат выполнеия)
    # вызывая метод .order_by('-datecompleted')
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=False).order_by('-datecompleted')
    context = {
        'todos': todos
    }

    return render(request, 'todo/completedtodo.html', context)
