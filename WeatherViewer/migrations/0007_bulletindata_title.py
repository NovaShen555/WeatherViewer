# Generated by Django 5.0.1 on 2024-04-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WeatherViewer", "0006_bulletindata"),
    ]

    operations = [
        migrations.AddField(
            model_name="bulletindata",
            name="title",
            field=models.CharField(default=8, max_length=50),
            preserve_default=False,
        ),
    ]
