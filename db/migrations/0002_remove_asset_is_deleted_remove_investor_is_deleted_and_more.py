# Generated by Django 5.0.2 on 2024-03-12 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='is_deleted',
        ),
    ]