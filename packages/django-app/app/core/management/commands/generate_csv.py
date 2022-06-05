import csv

from tqdm import tqdm

from common.management.commands.base_management_command import BaseManagementCommand
from core.repositories import LabelRepository, ImageRepository


class Command(BaseManagementCommand):
    """
    Generates a CSV of image filename and labels,
    to be consumed by our keras script.

    Most of the CSV headers will be defined from the labels that may exist.
    e.g. for the labels 'apples', 'oranges', 'bananas':
    +─────────────────+─────────+──────────+──────────+
    | filename        | apples  | oranges  | bananas  |
    +─────────────────+─────────+──────────+──────────+
    | fruit_bowl.jpg  | 1       | 1        | 0        |
    | grass.jpg       | 0       | 0        | 0        |
    | sundae.jpg      | 0       | 0        | 1        |
    +─────────────────+─────────+──────────+──────────+
    """

    # this is the directory where we will store the csv
    output_dir_path: str = 'media/training_data'

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        slugs = list(LabelRepository.get_by_filter().order_by(
            'slug').values_list('slug', flat=True))

        headers = ['filename'] + slugs

        images = ImageRepository.get_by_filter({'labels__isnull': False}).order_by('filename').prefetch_related(
            'labels').distinct()

        # open the file and create the file handler
        file_handler = open(f'{self.output_dir_path}/images_w_labels.csv', 'w')
        writer = csv.writer(file_handler)

        # write the first line
        if dry_run:
            self.stdout.write(str(headers))
        else:
            writer.writerow(headers)

        # write a line for each labeled image
        for image in tqdm(images):
            row = image.as_csv_row_w_labels(slugs)
            if dry_run:
                self.stdout.write(str(row))
            else:
                writer.writerow(row)

        file_handler.close()
