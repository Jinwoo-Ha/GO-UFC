# Generated by Django 4.2.15 on 2024-08-16 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_post_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight_class', models.CharField(max_length=50)),
                ('record', models.CharField(max_length=50)),
            ],
        ),
    ]
