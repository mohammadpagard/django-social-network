# Generated by Django 4.0.6 on 2022-07-30 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='post title', max_length=150),
        ),
    ]