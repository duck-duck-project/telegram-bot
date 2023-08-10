# Generated by Django 4.2.4 on 2023-08-10 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_can_be_added_to_contacts_and_more'),
        ('secret_messages', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretmedia',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.contact'),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
