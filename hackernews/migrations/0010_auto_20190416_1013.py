# Generated by Django 2.2 on 2019-04-16 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0009_auto_20190415_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='upvotes',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='hackernews.Comments'),
        ),
    ]
