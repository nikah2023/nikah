# Generated by Django 3.2.5 on 2023-01-30 03:19

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
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('М', 'М'), ('Ж', 'Ж')], default='М', max_length=1, verbose_name='sex')),
                ('birthday', models.DateTimeField(verbose_name='birthday')),
                ('nationality', models.CharField(max_length=64, verbose_name='nationality')),
                ('marital_status', models.CharField(max_length=64, verbose_name='marital_status')),
                ('amount_of_children', models.IntegerField(verbose_name='amount_of_children')),
                ('phone_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='phone_number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
                ('country', models.CharField(max_length=64, verbose_name='country')),
                ('city', models.CharField(max_length=64, verbose_name='city')),
                ('education', models.CharField(blank=True, max_length=64, null=True, verbose_name='education')),
                ('occupation', models.TextField(blank=True, null=True, verbose_name='person_occupation')),
                ('interests', models.TextField(blank=True, null=True, verbose_name='person_interests')),
                ('eye_color', models.CharField(blank=True, max_length=64, null=True, verbose_name='eye_color')),
                ('hair_color', models.CharField(blank=True, max_length=64, null=True, verbose_name='hair_color')),
                ('body_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='body_type')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='height')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='weight')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='avatar')),
                ('okay', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'person',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateTimeField(auto_now_add=True, verbose_name='dates')),
                ('title', models.CharField(max_length=256, verbose_name='title_status')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_person', to='marriage.person')),
            ],
            options={
                'db_table': 'status',
                'ordering': ['-dates'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datep', models.DateTimeField(auto_now_add=True, verbose_name='datep')),
                ('snapshot', models.ImageField(upload_to='images/', verbose_name='snapshot')),
                ('title', models.CharField(max_length=256, verbose_name='title_photo')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_person', to='marriage.person')),
            ],
            options={
                'db_table': 'photo',
                'ordering': ['-datep'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datem', models.DateTimeField(auto_now_add=True, verbose_name='datem')),
                ('details', models.TextField(blank=True, null=True, verbose_name='message_details')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_message', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
                'ordering': ['-datem'],
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datef', models.DateTimeField(auto_now_add=True, verbose_name='datef')),
                ('confirmation', models.BooleanField(default=False, verbose_name='confirmation')),
                ('amigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amigo_person', to='marriage.person')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_person', to='marriage.person')),
            ],
            options={
                'db_table': 'friend',
            },
        ),
        migrations.AddIndex(
            model_name='status',
            index=models.Index(fields=['person'], name='status_person__c419ed_idx'),
        ),
        migrations.AddIndex(
            model_name='status',
            index=models.Index(fields=['dates'], name='status_dates_491047_idx'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['person'], name='photo_person__cab147_idx'),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=models.Index(fields=['datep'], name='photo_datep_8406e4_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['user'], name='person_user_id_63ac75_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sender'], name='message_sender__0e912c_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['recipient'], name='message_recipie_5f6840_idx'),
        ),
        migrations.AddIndex(
            model_name='friend',
            index=models.Index(fields=['person'], name='friend_person__de4fb4_idx'),
        ),
    ]
