from django.db import connection


def db_health():

    try:

        connection.cursor()

        return True

    except:

        return False
