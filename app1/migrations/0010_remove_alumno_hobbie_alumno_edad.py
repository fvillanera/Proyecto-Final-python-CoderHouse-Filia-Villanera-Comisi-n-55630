# Generated by Django 4.2.4 on 2023-09-12 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_alumno_hobbie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno',
            name='hobbie',
        ),
        migrations.AddField(
            model_name='alumno',
            name='edad',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
