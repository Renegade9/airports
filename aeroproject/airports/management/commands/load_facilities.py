#
# Brute force ETL command to process the FAA facilities file into our Facility backend.
#
# Usage (as a Django administration command)
#
# python manage.py load_facilities --url=<url>
#
#     or
#
# python manage.py load_facilities --file=<filename>
#
# Option --dry-run can be used in both examples to echo the output without writing it to the DB.
#

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from airports.models import Facility
import csv
import pprint
import sys

AGENCY_CODE = 'FAA'
COUNTRY_CODE = 'USA'

class Command(BaseCommand):
    help = 'Loads the FAA Airports (Facilities) file into our backend'

    @staticmethod
    def convert_faa_geo(coordinate):
        """
        FAA files include geo coordinates in "decimal seconds" (e.g. 186780.8954N)...
        Convert to +/- decimal degrees.
        """
        last_char = coordinate[-1:]
        degrees = float(coordinate[:-1])/3600.0
        if last_char == 'S' or last_char == 'W':
            degrees *= -1.0
        return degrees

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

    def transform_facility(self, in_rec):
        '''
        Transforms an FAA facility record (dictionary format) into our Facility model.
        '''
        out_rec = {}

        try:
            out_rec['agency_code'] = AGENCY_CODE
            out_rec['country_code'] = COUNTRY_CODE
            out_rec['agency_site_key'] = in_rec['SiteNumber']

            # Local Airport Code
            if in_rec['LocationID']:
                if in_rec['LocationID'].startswith("'"):
                    out_rec['local_id'] = in_rec['LocationID'][1:]
                else:
                    out_rec['local_id'] = in_rec['LocationID']

            out_rec['facility_type'] = in_rec['Type']
            out_rec['effective_date'] = datetime.strptime(in_rec['EffectiveDate'],'%m/%d/%Y')
            out_rec['facility_name'] = in_rec['FacilityName']
            out_rec['city'] = in_rec['City']
            out_rec['elevation'] = in_rec['ARPElevation']
            out_rec['elevation_units'] = 'FT'

            if in_rec['TrafficPatternAltitude']:
                out_rec['tpa_agl'] = in_rec['TrafficPatternAltitude']
                out_rec['tpa_agl_units'] = 'FT'

            # Magnetic Variation
            if in_rec['MagneticVariation']:
                variation = in_rec['MagneticVariation']
                if variation.endswith('E') or variation.endswith('W'):
                    out_rec['magnetic_variation_degrees'] = variation[:-1]
                    out_rec['magnetic_variation_direction'] = variation[-1:]
                    if in_rec['MagneticVariationYear']:
                        out_rec['magnetic_variation_year'] = in_rec['MagneticVariationYear']

            if in_rec['CTAFFrequency']:
                out_rec['ctaf_frequency'] = in_rec['CTAFFrequency']

            out_rec['icao_id'] = in_rec['IcaoIdentifier']

            # Public Use?  If not one of the following codes, then leave null (unknown).
            if in_rec['Use'] == 'PU':
                out_rec['is_public_use'] = True
            elif in_rec['Use'] == 'PR':
                out_rec['is_public_use'] = False

            # N.B. Yes, an actual typo in the source data "Activiation" v. "Activation"
            if in_rec['ActiviationDate']:
                out_rec['activation_date'] = datetime.strptime(
                    in_rec['ActiviationDate'],'%m/%d/%Y')

            out_rec['latitude'] = self.convert_faa_geo(in_rec['ARPLatitudeS'])
            out_rec['longitude'] = self.convert_faa_geo(in_rec['ARPLongitudeS'])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        return out_rec

    def process_source(self, filename):

        records_processed = 0
        facilities_added = 0
        keys = []

        try:
            with open(filename) as tsv:
                for line in csv.reader(tsv, delimiter="\t"):

                    if not keys:  # first line
                        keys = line
                        continue

                    values = line
                    # make a dict of this record with the keys/header, and transform it
                    input_facility_d = dict(zip(keys, values))
                    output_facility_d = self.transform_facility(input_facility_d)

                    '''
                    print "-" * 80
                    pprint.pprint(input_facility_d)
                    pprint.pprint(output_facility_d)
                    '''

                    # Check for a match on agency_code + agency_site_key
                    result_set = Facility.objects.filter(
                        agency_code=AGENCY_CODE,
                        agency_site_key=output_facility_d['agency_site_key']
                    )

                    if len(result_set) == 0:
                        # Create the model instance from our dictionary
                        facility = Facility(**output_facility_d)
                        facility.save()
                        facilities_added += 1

                    records_processed += 1
                    if records_processed > 99999:
                        break
        except:
            print "Unexpected error processing file:", sys.exc_info()[0]
            raise

        self.stdout.write("Source records processed = %s" % records_processed)
        self.stdout.write("Facilities Added = %s" % facilities_added)

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



