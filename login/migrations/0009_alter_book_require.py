# Generated by Django 4.0.3 on 2022-07-28 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_remove_book_title_book_require'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='require',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
