import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_branch_manager_name'),
        ('inventory', '0004_remove_branch_transfer_state'),
        ('products', '0002_product_productimage_productlocation_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='BranchTransfer',
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
                            'transfer_number',
                            models.CharField(
                                max_length=50,
                                unique=True
                            )
                        ),
                        (
                            'status',
                            models.CharField(
                                choices=[
                                    ('PENDING', 'Pending'),
                                    ('IN_TRANSIT', 'In Transit'),
                                    ('RECEIVED', 'Received')
                                ],
                                default='PENDING',
                                max_length=20
                            )
                        ),
                        (
                            'transfer_date',
                            models.DateField()
                        ),
                        (
                            'created_by',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.PROTECT,
                                to=settings.AUTH_USER_MODEL
                            )
                        ),
                        (
                            'from_branch',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.PROTECT,
                                related_name='outgoing',
                                to='core.branch'
                            )
                        ),
                        (
                            'to_branch',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.PROTECT,
                                related_name='incoming',
                                to='core.branch'
                            )
                        ),
                    ],
                ),
                migrations.CreateModel(
                    name='BranchTransferItem',
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
                            'quantity',
                            models.DecimalField(
                                decimal_places=2,
                                max_digits=15
                            )
                        ),
                        (
                            'product',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.PROTECT,
                                to='products.product'
                            )
                        ),
                        (
                            'transfer',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to='core.branchtransfer'
                            )
                        ),
                    ],
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        'RENAME TABLE inventory_branchtransfer '
                        'TO core_branchtransfer'
                    ),
                    reverse_sql=(
                        'RENAME TABLE core_branchtransfer '
                        'TO inventory_branchtransfer'
                    ),
                ),
                migrations.RunSQL(
                    sql=(
                        'RENAME TABLE inventory_branchtransferitem '
                        'TO core_branchtransferitem'
                    ),
                    reverse_sql=(
                        'RENAME TABLE core_branchtransferitem '
                        'TO inventory_branchtransferitem'
                    ),
                ),
            ],
        ),
    ]
