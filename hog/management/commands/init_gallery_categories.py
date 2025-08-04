from django.core.management.base import BaseCommand
from hog.models import GalleryCategory

class Command(BaseCommand):
    help = 'Initialize gallery categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Christmas Light', 'slug': 'christmas-light'},
            {'name': 'Baby Dedication', 'slug': 'baby-dedication'},
            {'name': 'Weddings', 'slug': 'weddings'},
            {'name': "Pastor's Gallery", 'slug': 'pastor-gallery'},
            {'name': 'Church Gallery', 'slug': 'church-gallery'},
        ]

        for category in categories:
            GalleryCategory.objects.get_or_create(
                slug=category['slug'],
                defaults={'name': category['name']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category["name"]}"')
            )