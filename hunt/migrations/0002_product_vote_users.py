# Generated by Django 4.1.5 on 2023-02-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vote_users',
            field=models.TextField(default=''),
        ),
    ]