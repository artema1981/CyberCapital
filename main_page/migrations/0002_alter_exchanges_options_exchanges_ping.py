# Generated by Django 4.1.5 on 2023-01-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exchanges',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='exchanges',
            name='ping',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
