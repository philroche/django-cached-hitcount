import datetime
from django.core.management.base import NoArgsCommand
from cached_hitcount.utils import release_lock
from cached_hitcount.settings import CACHED_HITCOUNT_LOCK_KEY

class Command(NoArgsCommand):
    help = "Will delete the memcache lock used by hitcount"

    def handle_noargs(self, **options):
        release_lock()
