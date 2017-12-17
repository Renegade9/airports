#
# Brute force ETL command to process the FAA runways file into our Runway model.
#
# Usage (as a Django administration command)
#
# python manage.py load_runways --url=<url>
#
#     or
#
# python manage.py load_runways --file=<filename>
#
# Option --dry-run can be used in both examples to echo the output without writing it to the DB.
#

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from airports.models import Facility, Runway
import csv
import pprint
import sys

AGENCY_CODE = 'FAA'
COUNTRY_CODE = 'USA'

class Command(BaseCommand):
    help = 'Loads the FAA Runways file into our backend'

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

    def transform_runway(self, in_rec):
        '''
        Transforms an FAA runway record (dictionary format) into our Runway model.
        '''
        out_rec = {}

        try:
            # Get the facility PK that matches

            result_set = Facility.objects.filter(
                agency_site_key=in_rec['SiteNumber']
            )
            if len(result_set)==0:
                self.stdout.write(self.style.ERROR(
                    'Cannot find facility for site {}'.format(in_rec['SiteNumber'])))
                return None
            if len(result_set)>1:
                self.stdout.write(self.style.ERROR(
                    'Multiple facility matches for site {}'.format(in_rec['SiteNumber'])))
                return None

            out_rec['facility_id'] = result_set[0].pk
            out_rec['agency_site_key'] = in_rec['SiteNumber']
            out_rec['runway_id'] = in_rec['RunwayID'].lstrip("'")
            out_rec['runway_length'] = in_rec['RunwayLength']
            out_rec['runway_length_units'] = 'FT'  # because Merica
            out_rec['runway_width'] = in_rec['RunwayWidth']
            out_rec['runway_width_units'] = 'FT'  # because Merica
            out_rec['base_end_id'] = in_rec['BaseEndID'].lstrip("'")
            out_rec['reciprocal_end_id'] = in_rec['ReciprocalEndID'].lstrip("'")

            if in_rec['BaseEndRightTrafficPattern'] == 'Y':
                out_rec['base_end_traffic_dir'] = 'R'
            else:
                out_rec['base_end_traffic_dir'] = 'L'

            if in_rec['ReciprocalEndRightTrafficPattern'] == 'Y':
                out_rec['reciprocal_end_traffic_dir'] = 'R'
            else:
                out_rec['reciprocal_end_traffic_dir'] = 'L'

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        return out_rec

    def process_source(self, filename):

        records_processed = 0
        runways_added = 0
        keys = []

        try:
            with open(filename) as tsv:
                for line in csv.reader(tsv, delimiter="\t"):

                    if not keys:  # first line
                        keys = line
                        continue

                    values = line
                    # make a dict of this record with the keys/header, and transform it
                    input_runway_d = dict(zip(keys, values))
                    output_runway_d = self.transform_runway(input_runway_d)

                    """
                    print "-" * 80
                    pprint.pprint(input_runway_d)
                    pprint.pprint(output_runway_d)
                    """

                    if output_runway_d:
                        # Check for a match on agency_site_key + runway_id
                        result_set = Runway.objects.filter(
                            agency_site_key=output_runway_d['agency_site_key'],
                            runway_id=output_runway_d['runway_id']
                        )

                        if len(result_set) == 0:
                            # Create the model instance from our dictionary
                            runway = Runway(**output_runway_d)
                            runway.save()
                            runways_added += 1

                    records_processed += 1
                    if records_processed > 99999:
                        break
        except:
            print "Unexpected error processing file:", sys.exc_info()[0]
            raise

        self.stdout.write("Source records processed = %s" % records_processed)
        self.stdout.write("Runways Added = %s" % runways_added)

    def handle(self, *args, **options):

        dry_run = options['dry_run']

        # make sure either url or file option is present
        if options['url'] == None and options['file'] == None:
            raise CommandError("Option `--url=...` or `--file=...` must be specified.")

        if options['url'] != None:
            self.stdout.write("URL (--url) = %s" % options['url'])
            raise CommandError("Option `--url=...` not yet supported :(")

        if options['file'] != None:
            self.stdout.write("Filename (--file) = %s" % options['file'])

        if dry_run:
            self.stdout.write("Dry Run mode -- not saving to database")

        self.process_source(options['file'])

        self.stdout.write(self.style.SUCCESS('Alright, all done'))



