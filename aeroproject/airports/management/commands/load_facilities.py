from django.core.management.base import BaseCommand, CommandError
from airports.models import Facility as Airport

class Command(BaseCommand):
    help = 'Loads the FAA Airports (Facilities) file into our backend'

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            '--url',
            dest='url',
            help='URL of data source for Facilities',
        )
        parser.add_argument(
            '--file',
            dest='file',
            help='Facilities filename',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Dry Run (i.e. do not save)?',
        )


    def handle(self, *args, **options):

        # make sure either url or file option is present
        if options['url'] == None and options['file'] == None:
            raise CommandError("Option `--url=...` or `--file=...` must be specified.")

        if options['url'] != None:
            self.stdout.write("URL (--url) = %s" % options['url'])

        if options['file'] != None:
            self.stdout.write("Filename (--file) = %s" % options['file'])


        if options['dry_run']:
            self.stdout.write("Dry Run mode -- not saving to database")

        # Test that we can access our model
        all_airports = Airport.objects.all()
        print all_airports

        self.stdout.write(self.style.SUCCESS('Alright, all done'))



