# we arrive here from the 'urls.py' of our main project folder
# this file contains all urls, and respective functions that need to be called from 'views'
# also, we give each url a 'name', so that we can also refer to them by their name inside any html file or inside 'views' file

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('recipe/<str:pk>/', views.recipe, name="recipe"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-recipe/', views.createRecipe, name="create-recipe"),
    path('update-recipe/<str:pk>/', views.updateRecipe, name="update-recipe"),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name="delete-recipe"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user")
]
