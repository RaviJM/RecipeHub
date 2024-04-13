from django.forms import ModelForm
from .models import Recipe
from django.contrib.auth.models import User

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        # creates form for all fields we have defined in the model 'Recipe'
        fields = '__all__'
        exclude = ['host']
        

# for updating user
class UserForm(ModelForm):
    class Meta:
        model = User
        # creates form for fields we have defined in the model 'User' provided by django auth
        fields = ['username', 'email']
        # exclude = ['']

