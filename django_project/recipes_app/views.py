from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404
from random import sample, shuffle

from .forms import UserRegistrationForm, UserLoginForm, RecipeForm
from .models import Recipe


def index(request):
    all_recipes = Recipe.objects.filter(is_deleted=False)
    all_recipes = list(all_recipes)

    # Проверяем, достаточно ли рецептов для выбора пяти случайных
    if len(all_recipes) >= 5:
        # Если есть пять или более рецептов, выбираем пять случайных
        random_recipes = sample(list(all_recipes), 5)
    else:
        # Если рецептов меньше пяти, выбираем все доступные
        random_recipes = all_recipes

    shuffle(random_recipes)
    context = {
        'title': 'Главная',
        'recipes': random_recipes}
    return render(request, 'index.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('user_login')  # Перенаправление на страницу входа после успешной регистрации
        else:
            messages.info(request, 'Пользователь с таким именем уже существует.')
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, error.message)
            print(messages)
    else:
        form = UserRegistrationForm()

    content = {
        'title': 'Регистрация',
        'form': form,
    }

    return render(request, 'registration.html', content)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, error.message)
    else:
        form = UserLoginForm()

    content = {
        'title': 'Вход',
        'form': form,
    }

    return render(request, 'login.html', content)


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('index')


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipe_detail.html', context)


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт сохранен.')
            return redirect('my_recipes')
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, error.message)
    else:
        form = RecipeForm()

    content = {
        'title': 'Добавление рецепта',
        'form': form,
    }

    return render(request, 'recipe_form.html', content)


def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.author != request.user:
        raise Http404("У вас нет прав на редактирование этого рецепта.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт обновлен.')
            return redirect('recipe_detail', recipe_id=recipe.id)
        else:
            errors = form.errors.as_data()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, error.message)
    else:
        form = RecipeForm(instance=recipe)

    content = {
        'title': 'Редактирование рецепта',
        'form': form,
    }

    return render(request, 'recipe_form.html', content)


def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.author != request.user:
        raise Http404("У вас нет прав на удаление этого рецепта.")

    recipe.is_deleted = True
    recipe.save()
    messages.success(request, 'Рецепт удален.')
    return redirect('my_recipes')


def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user, is_deleted=False)
    context = {
        'title': 'Мои рецепты',
        'recipes': recipes}
    return render(request, 'recipes.html', context)


def all_recipes(request):
    recipes = Recipe.objects.filter(is_deleted=False)
    context = {
        'title': 'Все рецепты',
        'recipes': recipes}
    return render(request, 'recipes.html', context)


def my_deleted_recipes(request):
    recipes = Recipe.objects.filter(author=request.user, is_deleted=True)
    context = {'recipes': recipes}
    return render(request, 'my_deleted_recipes.html', context)


def recipe_restore(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.author != request.user:
        raise Http404("У вас нет прав на восстановление этого рецепта.")

    recipe.is_deleted = False
    recipe.save()
    messages.success(request, 'Рецепт восстановлен.')
    return redirect('my_deleted_recipes')