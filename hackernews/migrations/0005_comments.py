# Generated by Django 2.2 on 2019-04-09 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0004_newslinks_posted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('newslink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackernews.NewsLinks')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
