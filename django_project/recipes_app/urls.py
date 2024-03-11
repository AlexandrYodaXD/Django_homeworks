from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:recipe_id>/restore/', views.recipe_restore, name='recipe_restore'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('my_deleted_recipes/', views.my_deleted_recipes, name='my_deleted_recipes'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
]
