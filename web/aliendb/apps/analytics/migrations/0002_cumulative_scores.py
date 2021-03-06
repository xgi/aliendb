# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-20 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageNumComments',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('num_comments', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AverageScore',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubredditNumComments',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('num_comments', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubredditScore',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TotalNumComments',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('num_comments', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TotalScore',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='subreddit',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='subredditscore',
            name='subreddit',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='analytics.Subreddit'),
        ),
        migrations.AddField(
            model_name='subredditnumcomments',
            name='subreddit',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='analytics.Subreddit'),
        ),
    ]
