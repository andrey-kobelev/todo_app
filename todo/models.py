from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)

    # blank=True означает, что поле не обязательно к заполнению
    memo = models.TextField(blank=True)

    # DateTimeField - дата создания заметки
    # auto_now_add=True - будет означать,
    # что дата и время создадутся автоматически и
    # редактированию вручную не подлежит.
    created = models.DateTimeField(auto_now_add=True)  # данный отрибут поможет сортировать заметки.

    # добавить отметку о времени выполнения(завершения)
    datecompleted = models.DateTimeField(null=True, blank=True)

    # данный атрибут покажет галочк, нужна ли запись или нет
    # и выставим значение по умолчанию False (default=False)
    important = models.BooleanField(default=False)

    # создать привязку к пользователю, создав внешний ключ
    # он определит связь между записью и пользователем
    # то есть к записи присвоится id пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # показать заголовки прям в админке
    def __str__(self):
        return self.title
