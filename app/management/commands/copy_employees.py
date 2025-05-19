from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Copies employee data from other scheamas into public'

    def handle(self, *args, **options):

        with connection.cursor() as cursor:

            cursor.execute(
                        """
                        DO $$
                        DECLARE
                            schema_name TEXT;
                            insert_sql TEXT;
                        BEGIN
                            FOR schema_name IN
                                SELECT s.schema_name
                                FROM information_schema.schemata s
                                WHERE s.schema_name NOT IN ('public', 'information_schema')
                                  AND s.schema_name NOT LIKE 'pg_%'
                            LOOP
                                IF EXISTS (
                                    SELECT 1 
                                    FROM information_schema.tables 
                                    WHERE table_schema = schema_name 
                                    AND table_name = 'client_app_employee'
                                ) THEN
                                    insert_sql := format(
                                        'INSERT INTO public.app_clientemployee (first_name, last_name, tenant_id)
                                         SELECT first_name, last_name, tenant_id FROM %I.client_app_employee',
                                        schema_name
                                    );
                                    RAISE NOTICE 'Executing: %', insert_sql;
                                    EXECUTE insert_sql;
                                ELSE
                                    RAISE NOTICE 'Skipping schema %: table client_app_employee not found', schema_name;
                                END IF;
                            END LOOP;
                        END $$;
                        """)

            print("DONE")