# Generated by Django 5.0.4 on 2024-07-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_student_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
