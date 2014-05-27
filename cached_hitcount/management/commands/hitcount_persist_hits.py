import datetime
from django.core.management.base import NoArgsCommand
from cached_hitcount.tasks import persist_hits

class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to persist_hits to the database."

    def handle_noargs(self, **options):
        persist_hits()
