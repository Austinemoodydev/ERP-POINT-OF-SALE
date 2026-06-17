import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_branch_is_active_branch_active_branchuser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchRole',
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
                    'name',
                    models.CharField(
                        max_length=100
                    )
                ),
                (
                    'description',
                    models.TextField(
                        blank=True
                    )
                ),
                (
                    'active',
                    models.BooleanField(
                        default=True
                    )
                ),
                (
                    'branch',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='core.branch'
                    )
                ),
            ],
            options={
                'unique_together': {('branch', 'name')},
            },
        ),
    ]
