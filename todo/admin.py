from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    """ данный класс наследован от model admin
    добавляем атрибут readonly_fields со значением created(имя атрибута класса _Todo_)
    что бы в админке просто отражалась дата создания записи."""

    readonly_fields = ('created',)


admin.site.register(Todo, TodoAdmin)
