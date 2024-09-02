# Generated by Django 5.0.6 on 2024-08-05 11:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fypapp', '0007_remove_shelter_password'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.CharField(choices=[('adopter', 'Adopter'), ('shelter', 'Shelter')], max_length=10)),
                ('adopterid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fypapp.adopter')),
                ('shelterid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fypapp.shelter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
