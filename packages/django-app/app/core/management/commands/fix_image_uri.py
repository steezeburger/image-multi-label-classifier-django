from django.core.management.base import BaseCommand

from core.models import Image


class Command(BaseCommand):
    """
    Removes "media/" part from Image.uri values.
    I needed to fix this after properly configuring MEDIA_URL.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry_run',
            help='Run script with out saving changes to database.',
            action='store_true'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        for image in Image.objects.all():
            new_uri = image.uri.replace('media/', '')
            self.stdout.write(f'{image.uri} ---> {new_uri}')

            if not dry_run:
                image.uri = new_uri
                image.save()
