from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fintech', '0002_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='is_staff_role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
