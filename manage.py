#!/usr/bin/env python

import os
import sys
from time import sleep
import django.db

if __name__ == "__main__":
    MAX_RETRIES_NUM = 15

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangodocker.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    retry_num = 1
    executed_successfully = False

    while (not executed_successfully) and (retry_num <= MAX_RETRIES_NUM):
        try:
            execute_from_command_line(sys.argv)
            executed_successfully = True

        except django.db.utils.OperationalError as exc:
            if 'could not connect to server: Connection refused' in str(exc):
                print(
                    'DATABASE EXCEPTION: Database is not yet accepting connections. ',
                    'Sleeping for 1 second...',
                )
            elif 'the database system is starting up' in str(exc):
                print(
                    'DATABASE EXCEPTION: Database is starting up. ',
                    'Sleeping for 1 second...',
                )
            else:
                print('WARNING! Unhandled <django.db.utils.OperationalError>!')
                raise
            sleep(1)
            retry_num += 1
