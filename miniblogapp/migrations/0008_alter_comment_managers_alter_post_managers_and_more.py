# Generated by Django 4.0.6 on 2022-08-04 11:46

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('miniblogapp', '0007_alter_post_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='comment',
            managers=[
                ('comment_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
