
from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate

class Command(BaseCommand):
    help = 'Seeds the database with detailed descriptions for the Reincarnation Cycle.'

    def handle(self, *args, **options):
        reincarnation_cycle_periods = [
            {
                "period_number": 1,
                "description": "Childhood and the soul's descent into the body. The personality is latent."
            },
            {
                "period_number": 2,
                "description": "Adolescence and the awakening of personality. The ego begins to assert itself."
            },
            {
                "period_number": 3,
                "description": "Early adulthood and the soul's struggle for expression. The personality is dominant."
            },
            {
                "period_number": 4,
                "description": "Maturity and the soul's search for meaning. The personality begins to yield to the soul."
            },
            {
                "period_number": 5,
                "description": "Mid-life and the soul's illumination. The personality is now a vehicle for the soul."
            },
            {
                "period_number": 6,
                "description": "Later life and the soul's detachment from the physical world. The personality is transcended."
            },
            {
                "period_number": 7,
                "description": "Old age and the soul's return to its source. The personality is dissolved."
            },
            {
                "period_number": 8,
                "description": "The soul's journey through the spiritual worlds. The personality is a distant memory."
            },
            {
                "period_number": 9,
                "description": "The soul's assimilation of its earthly experiences. The personality is completely absorbed."
            },
            {
                "period_number": 10,
                "description": "The soul's choice of a new destiny. The personality is a seed of future potential."
            },
            {
                "period_number": 11,
                "description": "The soul's preparation for rebirth. The personality is a blueprint for the new life."
            },
            {
                "period_number": 12,
                "description": "The soul's descent into a new body. The personality is a fresh canvas."
            }
        ]

        for period_data in reincarnation_cycle_periods:
            CycleTemplate.objects.update_or_create(
                cycle_type='reincarnation',
                period_number=period_data['period_number'],
                defaults={'description': period_data['description']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded detailed descriptions for the Reincarnation Cycle.'))
