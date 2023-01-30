from django.forms import ModelForm
from .models import Todo


# создать свою форму(class) наследуемую от ModelForm
class TodoForm(ModelForm):
    class Meta:

        # указать модель для объектов Todo
        model = Todo

        # Что мы будем отображать? В списке указать список отрибутов,
        # котрые нужно отобразить из Todo Models
        fields = ['title', 'memo', 'important']
