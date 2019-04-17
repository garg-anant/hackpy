# Generated by Django 2.2 on 2019-04-15 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0007_auto_20190414_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslinks',
            name='base_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hackernews.Comments'),
        ),
    ]
