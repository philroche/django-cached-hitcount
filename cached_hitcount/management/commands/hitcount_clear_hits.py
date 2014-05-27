from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from cached_hitcount.models import Hit
from cached_hitcount.management.helpers import prompt_bool

'''
python manage.py hitcount_clear_hits --from='2014-05-27' --to='2014-05-27'
'''
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--from',  dest='from_date', action='store', type="string", default=None, help='Datetime from (incl.)'),
        make_option('--to',  dest='to_date', action='store', type="string", default=None, help='Datetime up to (incl.)'),
    )
    help = "Will delete all existing hits"
    def handle(self, **options):
        from_date  = options.get('from_date', None)
        to_date  = options.get('to_date', None)

        hits = Hit.objects.all()

        if from_date is not None:
            parsed_from_date = datetime.strptime( from_date, "%Y-%m-%d" )
            hits = hits.filter(added__gte = parsed_from_date)
        if to_date is not None:
            parsed_to_date = datetime.strptime( to_date, "%Y-%m-%d" )
            hits = hits.filter(added__lte = parsed_to_date)

        print hits.query
        if prompt_bool("Are you sure you want to delete all selected %d hits" % hits.count()):
            hits.delete()
            print "All selected hits have been deleted"


