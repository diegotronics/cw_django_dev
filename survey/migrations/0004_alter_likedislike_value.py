# Generated by Django 3.2.5 on 2023-11-21 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_alter_likedislike_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedislike',
            name='value',
            field=models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')], default=1, verbose_name='Like/Dislike'),
        ),
    ]
