from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from products.models import Product

# (name, description, price, stock)
SEED_PRODUCTS = [
    ("Mechanical Keyboard", "Hot-swappable 75% keyboard with tactile switches.", "79.90", 45),
    ("Wireless Mouse", "Ergonomic 2.4 GHz mouse with silent clicks.", "24.50", 120),
    ("USB-C Hub 7-in-1", "HDMI, USB-A, SD card reader, and 100W power delivery.", "39.00", 80),
    ("27-inch 4K Monitor", "IPS panel, 60 Hz, USB-C connectivity.", "329.00", 15),
    ("Laptop Stand", "Adjustable aluminium stand for 11 to 17 inch laptops.", "29.99", 60),
    ("Noise-Cancelling Headphones", "Over-ear Bluetooth headphones, 30-hour battery.", "149.00", 30),
    ("Webcam 1080p", "Full HD webcam with built-in microphone and privacy cover.", "49.90", 55),
    ("Portable SSD 1TB", "USB 3.2 external SSD, up to 1000 MB/s read speed.", "94.50", 40),
    ("Ergonomic Office Chair", "Mesh back, adjustable lumbar support and armrests.", "219.00", 12),
    ("LED Desk Lamp", "Dimmable lamp with adjustable colour temperature.", "22.75", 90),
    ("Bluetooth Speaker", "Portable waterproof speaker, 12-hour playtime.", "35.00", 70),
    ("Power Bank 20000mAh", "Dual-port fast-charging power bank.", "32.40", 100),
    ("HDMI Cable 2m", "High-speed HDMI 2.1 cable.", "8.99", 200),
    ("Smartwatch", "Fitness tracking, heart-rate monitor, 7-day battery.", "119.00", 0),
    ("Wireless Charger Pad", "15W Qi wireless charging pad.", "18.50", 85),
]


class Command(BaseCommand):
    help = "Seed the database with sample products. Safe to run repeatedly."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete ALL existing products before seeding.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allow seeding when DEBUG is False (e.g. staging).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to seed while DEBUG is False. Use --force if you really mean it."
            )

        if options["reset"]:
            deleted, _ = Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing product(s)."))

        created_count = 0
        updated_count = 0

        for name, description, price, stock in SEED_PRODUCTS:
            _, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": Decimal(price),
                    "stock": stock,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} created, {updated_count} updated."
            )
        )