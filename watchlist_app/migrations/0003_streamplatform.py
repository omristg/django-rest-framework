# Generated by Django 5.0.6 on 2024-05-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0002_watchlist_delete_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('about', models.CharField(max_length=150)),
                ('website', models.CharField(max_length=100)),
            ],
        ),
    ]