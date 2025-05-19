from django.conf import settings
from django.core.management.base import BaseCommand
import subprocess
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Backup the PostgreSQL database'

    def handle(self, *args, **options):
        db_name = os.getenv('DB_NAME', settings.DATABASES['default']['NAME'])
        db_user = os.getenv('DB_USER', settings.DATABASES['default']['USER'])
        db_password = os.getenv('DB_PASSWORD', settings.DATABASES['default']['PASSWORD'])
        db_host = os.getenv('DB_HOST', settings.DATABASES['default'].get('HOST', 'localhost'))

        output_dir = Path('app/management/commands/backups')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f'{db_name}_backup.dump'

        command = [
            'pg_dump',
            '-U', db_user,
            '-h', db_host,
            '-Fc',
            '-f', str(output_file),
            db_name,
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        try:
            subprocess.run(command, check=True, env=env)
            self.stdout.write(self.style.SUCCESS(f'Backup saved to {output_file}'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Backup failed: {e}'))