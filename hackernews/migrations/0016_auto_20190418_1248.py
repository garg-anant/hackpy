# Generated by Django 2.2 on 2019-04-18 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0015_auto_20190417_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hackernews.Comments'),
        ),
        migrations.AlterField(
            model_name='newslinks',
            name='hackernews_post_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='upvotescomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackernews.Comments'),
        ),
    ]
