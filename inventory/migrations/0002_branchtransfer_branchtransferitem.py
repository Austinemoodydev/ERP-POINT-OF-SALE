import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_branch_is_active_branch_active_branchuser_and_more'),
        ('inventory', '0001_initial'),
        ('products', '0002_product_productimage_productlocation_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                        to='inventory.branchtransfer'
                    )
                ),
            ],
        ),
    ]
