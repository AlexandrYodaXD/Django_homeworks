# Generated by Django 5.0.2 on 2024-03-11 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0003_recipe_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='categories',
            new_name='category',
        ),
    ]
