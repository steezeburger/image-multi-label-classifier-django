from common.management.commands.base_management_command import BaseManagementCommand
from core.models import Image


class Command(BaseManagementCommand):
    """
    Removes "media/" part from Image.uri values.
    I needed to fix this after properly configuring MEDIA_URL.
    """

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        for image in Image.objects.all():
            new_uri = image.uri.replace('media/', '')
            self.stdout.write(f'{image.uri} ---> {new_uri}')

            if not dry_run:
                image.uri = new_uri
                image.save()
