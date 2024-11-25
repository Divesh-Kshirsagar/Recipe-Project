from django.contrib import admin
from django.urls import path
from . import views

app_name = "Home"

urlpatterns = [
    path('', views.index, name='index'),
    path('all_recipe/', views.all_recipe, name='all_recipe'),
    path('user_recipe/', views.user_recipe, name='user_recipe'),
    path('delete_recipe/<int:id>', views.delete_recipe, name='delete_recipe'),
    path('update_recipe/<int:id>', views.update_recipe, name='update_recipe'),
    path('recipe/<int:id>', views.recipe, name='recipe'),
]
