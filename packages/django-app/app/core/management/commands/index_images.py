import json
import os
from typing import Optional

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from core.management.helpers import get_file_contents, write_file_contents
from core.repositories import ImageRepository


class Command(BaseCommand):
    """
    Indexes the images in media/images.

    Images should be .jpg
    If there is a .txt file with the same filename as the image, it will be used
      for a description.
    """

    images_dir_path: str = 'media/images'

    def get_uri_for_filename(self, filename: str) -> str:
        uri = f"{self.images_dir_path}/{filename}"
        return uri

    def get_description_text_for_filename(self, filename: str) -> Optional[str]:
        """
        Finds the .txt file with the same filename and returns the contents, or None.
        """
        text_filename = f"{filename.split('.')[0]}.txt"
        text_uri = self.get_uri_for_filename(text_filename)
        if os.path.exists(text_uri):
            contents = get_file_contents(text_uri)
            if contents:
                contents = str.replace(contents, "\x00", "", -1)
                return contents

        return None

    def handle(self, *args, **options):
        results_path = 'media/processed.json'

        try:
            previously_processed = get_file_contents(results_path)
            previously_processed = json.loads(previously_processed)
        except FileNotFoundError:
            # if the file doesn't exist, just use an empty list.
            # we write the entire file at the end,
            #   so we don't need to worry about creating it here.
            previously_processed = []

        report_dict = {
            'images_processed': 0,
            'filenames_processed': [],
        }
        self.stdout.write('Begin indexing images...')

        try:
            for filename in os.listdir(self.images_dir_path):
                if report_dict['images_processed'] % 10 == 0:
                    self.stdout.write(f"processed {report_dict['images_processed']} images...")

                if filename.endswith('.txt'):
                    continue

                if filename in previously_processed:
                    continue

                image_data = {
                    'filename': filename,
                    'uri': self.get_uri_for_filename(filename),
                    'description': self.get_description_text_for_filename(filename),
                }
                try:
                    image = ImageRepository.create(image_data)
                    report_dict['images_processed'] += 1
                    report_dict['filenames_processed'].append(image.filename)
                except IntegrityError as e:
                    print(e)
                    pass
        except Exception as e:
            raise e
        finally:
            all_processed = previously_processed + report_dict['filenames_processed']
            write_file_contents(
                results_path,
                json.dumps(all_processed))
            self.stdout.write(f"{report_dict['images_processed']} images processed!")
