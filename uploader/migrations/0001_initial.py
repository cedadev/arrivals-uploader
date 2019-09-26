# Generated by Django 2.0.5 on 2018-06-01 11:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-_]*$', 'Only alphanumeric characters and hyphens/underscores are allowed.')])),
                ('stream_type', models.IntegerField(choices=[('UNKNOWN', 0), ('BASIC', 1)], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UploaderProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_directory', models.TextField(blank=True)),
                ('visible_ftp_password', models.TextField(blank=True)),
                ('visible_rsync_password', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='stream',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploader.UploaderProfile'),
        ),
    ]