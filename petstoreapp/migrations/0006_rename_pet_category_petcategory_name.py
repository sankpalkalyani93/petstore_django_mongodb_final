# Generated by Django 5.0.1 on 2024-02-19 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petstoreapp', '0005_alter_pet_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petcategory',
            old_name='pet_category',
            new_name='name',
        ),
    ]
