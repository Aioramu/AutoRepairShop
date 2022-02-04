# Generated by Django 3.2.12 on 2022-02-03 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=None, null=True)),
                ('specialist', models.CharField(choices=[('motor', 'Мастер по моторам'), ('universal', 'Мастер по общим работам'), ('suspension', 'Мастер по обслуживанию подвески'), ('transmission', 'Мастер по кпп')], max_length=255)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
