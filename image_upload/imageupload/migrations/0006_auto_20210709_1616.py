# Generated by Django 3.1.7 on 2021-07-09 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageupload', '0005_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='after_predict',
            field=models.FileField(default=1, upload_to='predict_video/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
