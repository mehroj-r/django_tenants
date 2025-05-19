from django.conf import settings
from django.core.management.base import BaseCommand
import subprocess
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Restore the PostgreSQL database from a backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='backup_file',
            help='Specific backup file to restore (optional)'
        )

    def handle(self, *args, **options):
        db_name = os.getenv('DB_NAME', settings.DATABASES['default']['NAME'])
        db_user = os.getenv('DB_USER', settings.DATABASES['default']['USER'])
        db_password = os.getenv('DB_PASSWORD', settings.DATABASES['default']['PASSWORD'])
        db_host = os.getenv('DB_HOST', settings.DATABASES['default'].get('HOST', 'localhost'))

        # Determine which backup file to use
        backup_dir = Path('app/management/commands/backups')
        if options['backup_file']:
            backup_file = Path(options['backup_file'])
            if not backup_file.is_absolute():
                backup_file = backup_dir / backup_file
        else:
            # Use the latest backup for this database if no specific file is provided
            backup_file = backup_dir / f'{db_name}_backup.dump'

        # Check if backup file exists
        if not backup_file.exists():
            self.stderr.write(self.style.ERROR(f'Error: Backup file {backup_file} does not exist'))
            return

        self.stdout.write(f'Restoring database {db_name} from {backup_file}')

        # Get confirmation from user unless a specific backup file was requested
        if not options['backup_file']:
            confirm = input(f'This will overwrite the current {db_name} database. Continue? (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write('Restore cancelled.')
                return

        # The restore command using pg_restore
        command = [
            'pg_restore',
            '-U', db_user,
            '-h', db_host,
            '-d', db_name,
            '--clean',  # Clean database objects before recreating
            '--if-exists',  # Don't error if objects don't exist
            '--no-owner',  # Don't recreate the same object ownership
            str(backup_file)
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        try:
            subprocess.run(command, check=True, env=env)
            self.stdout.write(self.style.SUCCESS(f'Database {db_name} successfully restored from {backup_file}'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Restore failed: {e}'))