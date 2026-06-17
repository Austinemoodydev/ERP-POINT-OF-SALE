import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_branch_code_branch_manager_name_alter_branch_address_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='is_active',
            new_name='active',
        ),
        migrations.AlterField(
            model_name='branch',
            name='code',
            field=models.CharField(
                max_length=20,
                unique=True
            ),
        ),
        migrations.CreateModel(
            name='BranchUser',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'is_default',
                    models.BooleanField(
                        default=False
                    )
                ),
                (
                    'branch',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='core.branch'
                    )
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
        ),
    ]
