# Generated by Django 5.0.1 on 2024-02-19 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petstoreapp', '0007_alter_pet_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PetCategory',
        ),
    ]
