# Generated by Django 3.2.5 on 2021-07-05 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="status",
            field=models.CharField(
                choices=[
                    ("layoffs", "Layoffs"),
                    ("Hiring Freeze", "Hiring Freeze"),
                    ("Hiring", "Hiring"),
                ],
                default="Hiring",
                max_length=30,
            ),
        ),
    ]
