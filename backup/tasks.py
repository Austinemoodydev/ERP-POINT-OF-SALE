
from celery import shared_task


@shared_task
def backup_database():

    import os

    os.system(



        'mysqldump -u root poserp > backup.sql'


    )
