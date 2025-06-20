# Generated by Django 5.2.1 on 2025-06-18 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('query_id', models.CharField(max_length=255, unique=True)),
                ('city_name', models.CharField(max_length=45)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
