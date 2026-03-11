from django.core.management.base import BaseCommand

from dashboard.faker import generate_demo_data


class Command(BaseCommand):
    help = "Populate the database with realistic demo data for DocuClinic."

    def handle(self, *args, **options):
        self.stdout.write("Generating demo data. This may take a moment...")
        generate_demo_data()
        self.stdout.write(self.style.SUCCESS("Demo data generated successfully."))
