# Generated by Django 3.1.2 on 2020-10-28 10:22

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
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(blank=True, max_length=100, null=True)),
                ('question_hin', models.CharField(max_length=200)),
                ('correct_answer', models.CharField(max_length=200)),
                ('reference', models.URLField()),
                ('question_eng', models.CharField(max_length=200)),
                ('correctness_score', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trust_score', models.FloatField(default=0)),
                ('last_test_score', models.FloatField(default=0)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_pic', models.ImageField(upload_to='uploads/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100)),
                ('confidence_score', models.FloatField(default=0)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.question')),
            ],
        ),
    ]
