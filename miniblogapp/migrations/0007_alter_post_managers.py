# Generated by Django 4.0.6 on 2022-08-03 14:51

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('miniblogapp', '0006_post_is_deleted_alter_post_image_alter_profile_image'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('post_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
