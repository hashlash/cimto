from django.core.management.base import BaseCommand

from cimto.importer.kujawab import KujawabSiteImporter


class Command(BaseCommand):
    def handle(self, *args, **options):
        imp = KujawabSiteImporter()
        imp.import_data()
