# 'views' contains methods/ functions, that are called according to url inside 'urls.py'
# these methods/ functions fetch data from 'models.py' and return the respective template page (html page) from 'templates' folder
# each function handles 2 kinds of data (before the 'return' line), which is: about the data that is required to be load in the webpage, and the data that is coming from the webpage in the form of response, which simply means the form data (like updating recipe, or creating user or login or anything)

from django.shortcuts import render, redirect
from .models import Recipe, Topic, Message
from .forms import RecipeForm, UserForm
from django.http import HttpResponse

# for login/logout/authentication purposes, we import in-built functionalities
from django.contrib.auth import authenticate, login, logout

# for login/ registration purpose, we import the in-built 'User' model
from django.contrib.auth.models import User

# for flashing messages
from django.contrib import messages

# for advanced searching
from django.db.models import Q

# for 'restricting-pages' to users, if they are not logged in and try to access any functionality of the project (needs to be added to each functionality separately)
from django.contrib.auth.decorators import login_required

# in-built user creation form, used for 'registering' a new user
from django.contrib.auth.forms import UserCreationForm





def loginPage(request):
    
    # page's name
    page = 'login'
    
    if request.user.is_authenticated:   #if you are logged-in, and still try to access the url /login then you cannot, and are redirected to homepage
        return redirect('home')

    if request.method == 'POST':
        
        # get the usename and password
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check if user exists (during login, that is)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # authenticate
        user = authenticate(request, username=username, password=password)

        # login if exist
        if user is not None:
            # call in-built login functionality, that uses session, it creates a session id
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or Password does not exist!')
    context = {'page': page}
    return render(request, 'login_register.html', context)



def logoutUser(request):
    logout(request)     # this function call deletes the session or token, so that the user is no more authenticated
    return redirect('home')



# for new user registration
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    
    return render(request, 'login_register.html', {'form': form})



# homepage
def home(request):

    # to display the topics as per the 'topic' that the user clicks on (done using filter)
    # for 'ALL' in 'topics', the value of p is empty string ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    recipes = Recipe.objects.filter(
        Q(topic__name__icontains=q) |   # search by topic name
        Q(name__icontains=q) |          # search by recipe
        Q(description__icontains=q)     # search by description of recipe
    )

    # get all the topics from database
    topics = Topic.objects.all()
    
    recipe_count = recipes.count()

    context = {'recipes': recipes, 'topics': topics, 'recipe_count': recipe_count}
    
    return render(request, 'home.html', context)



# when user clicks on any recipe (inside recipe)
def recipe(request, pk):

    # get the recipe that is clicked
    recipe = Recipe.objects.get(id=pk)

    # get all the comments (messages) for that recipe (from the model)
    recipe_messages = recipe.message_set.all().order_by('-created')     # order_by(...) is used to get recent messages to top
    
    if request.method == 'POST':
        message = Message.objects.create(   # this creates an entry in the model 'Message' (method-create)
            user = request.user,
            recipe = recipe,
            body = request.POST.get('body')   #what we received from the 'add-comment' form
        )
        return redirect('recipe', pk=recipe.id)
    
    context = {'recipe': recipe, 'recipe_messages': recipe_messages}
    return render(request, 'recipe.html', context)



def userProfile(request, pk):
    # get user from model
    user = User.objects.get(id=pk)
    
    # get all his recipes
    recipes = user.recipe_set.all()
    topics = Topic.objects.all()
    
    context = {'user': user, 'recipes': recipes, 'topics': topics}
    return render(request, 'profile.html', context)



# for creating recipe
@login_required(login_url='login')    #this redirects user to login page if they try to access the below written functionality (prompting them to login if they want to access the functionality)
def createRecipe(request):
    form = RecipeForm()
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Recipe.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    
    return render(request, 'recipe_form.html', context)



# for updating a recipe
@login_required(login_url='login')    #this redirects user to login page (if not logged in) if they try to access the below written functionality (prompting them to login if they want to access the functionality)
def updateRecipe(request, pk):
    # gets the info about recipe
    recipe = Recipe.objects.get(id=pk)

    # to pre-fill the empty form with values of the recipe we are going to update
    form = RecipeForm(instance=recipe)
    
    # getting list of all topics
    topics = Topic.objects.all()


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        recipe.name = request.POST.get('name')
        recipe.topic = topic
        recipe.description = request.POST.get('description')
        recipe.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'recipe': recipe}
    return render(request, 'recipe_form.html', context)



# to delete a recipe
@login_required(login_url='login')    #this redirects user to login page if they try to access the below written functionality (prompting them to login if they want to access the functionality)
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if request.method == 'POST':
        recipe.delete()     # removes from database
        return redirect('home')
    
    return render(request, 'delete.html', {'obj': recipe})



# to delete a message (comment)
@login_required(login_url='login')    #this redirects user to login page if they try to access the below written functionality (prompting them to login if they want to access the functionality)
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj': message})



# for updating user profile
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    
    # to pre-fill the empty form with values of the user form we are going to update
    form = UserForm(instance=user)
    context = {'form': form}
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk = user.id)
        
    return render(request, 'update_user.html', context)
