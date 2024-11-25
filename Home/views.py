from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


def index(request):
    return render(request, 'Home/index.html')


@login_required
def user_recipe(request):
    data = request.POST
    if request.method == "POST":
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_img = request.FILES.get('recipe_img')
        
        Recipe.objects.create(
            user=request.user,
            recipe_img = recipe_img,
            recipe_name = recipe_name,
            recipe_description = recipe_description,
        )
        
        return render(request, 'Home/user_recipe.html')
    
    user = request.user
    queryset = Recipe.objects.filter(user=user)
    
    paginator = Paginator(queryset,5)
    page_number = request.GET.get('page')
    pag_obj = paginator.get_page(page_number)

    context = {'recipes':pag_obj}
    
    return render(request, 'Home/user_recipe.html', context)


def all_recipe(request):
    queryset = Recipe.objects.all()
    
    paginator = Paginator(queryset,5)
    page_number = request.GET.get('page')
    pag_obj = paginator.get_page(page_number)

    context = {'recipes':pag_obj}
    return render(request, 'Home/all_recipe.html', context)

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    context = {'recipe':recipe}
    return render(request, 'Home/recipe.html', context)

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Post deleted successfully.')
    return redirect('Home:user_recipe')

def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    data = request.POST
    if request.method == "POST":
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_img = request.FILES.get('recipe_img')
        
        recipe.recipe_name = recipe_name
        recipe.recipe_description = recipe_description
        
        if recipe_img:
            recipe.recipe_img = recipe_img
            
        recipe.save()
        return redirect('/user_recipe')
    context = {'recipe':recipe}
    return render(request, 'Home/update_recipe.html', context)
