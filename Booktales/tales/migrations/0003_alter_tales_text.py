# Generated by Django 5.1.3 on 2024-12-06 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tales', '0002_alter_tales_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tales',
            name='text',
            field=models.TextField(max_length=240),
        ),
    ]
