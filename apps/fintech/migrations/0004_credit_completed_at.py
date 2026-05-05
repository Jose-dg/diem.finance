from django.db import migrations, models


def backfill_completed_at(apps, schema_editor):
    Credit = apps.get_model('fintech', 'Credit')
    Credit.objects.filter(state='completed', completed_at__isnull=True).update(
        completed_at=models.F('updated_at')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('fintech', '0003_remove_role_is_staff_role_and_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(backfill_completed_at, migrations.RunPython.noop),
    ]
