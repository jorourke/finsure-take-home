# Generated by Django 4.1.7 on 2023-03-27 04:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lender",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=20)),
                ("upfront_commission_rate", models.FloatField()),
                ("trial_commission_rate", models.FloatField()),
                ("active", models.BooleanField(default=True)),
            ],
        ),
    ]
