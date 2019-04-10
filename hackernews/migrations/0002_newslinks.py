# Generated by Django 2.2 on 2019-04-08 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('title_link', models.CharField(max_length=500)),
                ('num_comments', models.PositiveIntegerField(default=0)),
                ('hackernews_post_id', models.PositiveIntegerField(unique=True)),
                ('upvotes', models.PositiveSmallIntegerField(default=0)),
                ('downvotes', models.PositiveSmallIntegerField(default=0)),
                ('karma_points', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
