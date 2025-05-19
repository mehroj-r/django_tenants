# myapp/management/commands/drop_schemas.py
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Drop all schemas except public and system schemas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List schemas that would be dropped without actually dropping them',
        )

    @transaction.atomic
    def handle(self, *args, **options):

        # Get list of all schemas that aren't system schemas or public
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT schema_name
                           FROM information_schema.schemata
                           WHERE schema_name NOT IN
                                 ('public', 'information_schema', 'pg_catalog', 'pg_toast', 'pg_temp_1',
                                  'pg_toast_temp_1')
                             AND schema_name NOT LIKE 'pg_%'
                           """)
            schemas_to_drop = [row[0] for row in cursor.fetchall()]

        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f'Would drop {len(schemas_to_drop)} schemas:'))
            for schema in schemas_to_drop:
                self.stdout.write(f"  - {schema}")
            return

        # Drop each schema
        with connection.cursor() as cursor:
            for schema_name in schemas_to_drop:
                self.stdout.write(f"Dropping schema: {schema_name}")
                # Drop schema with CASCADE to remove all objects in it
                cursor.execute(f'DROP SCHEMA {schema_name} CASCADE')

        self.stdout.write(self.style.SUCCESS(f'Successfully dropped {len(schemas_to_drop)} schemas'))