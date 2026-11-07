import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.countries.models import Country

DATA_FILE = Path(settings.BASE_DIR) / "data" / "countries.json"


class Command(BaseCommand):
    help = "Carga países desde data/countries.json de forma idempotente."

    def handle(self, *args, **options):
        if not DATA_FILE.exists():
            raise CommandError(f"No existe {DATA_FILE}")

        rows = json.loads(DATA_FILE.read_text(encoding="utf-8"))

        created = updated = 0
        for row in rows:
            _, was_created = Country.objects.update_or_create(
                iso_code=row["iso_code"],
                defaults={
                    "name": row["name"],
                    "capital": row["capital"],
                    "region": row.get("region", ""),
                },
            )
            created += was_created
            updated += not was_created

        self.stdout.write(
            self.style.SUCCESS(f"{created} creados, {updated} actualizados")
        )
