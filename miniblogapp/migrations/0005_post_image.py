# Generated by Django 4.0.6 on 2022-08-02 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblogapp', '0004_alter_comment_email_alter_comment_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='post'),
        ),
    ]
