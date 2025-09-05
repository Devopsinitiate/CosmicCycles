from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate

class Command(BaseCommand):
    help = 'Seeds the database with detailed descriptions for the Health Cycle.'

    def handle(self, *args, **options):
        health_cycle_periods = [
            {
                "period_number": 1,
                "description": "During this period the vitality and constitutional health should be at its best and, if it is below normal, it will be more quickly and easily increased and strengthened by normal living and the avoidance of the violation of any natural laws. Plenty of outdoor walking, good air, drinking plenty of water and eating proper foods, avoiding foods that are overheating, especially the starches and raw or rare meats—this will yield results. The eyes should be guarded against overuse or use in bright electric lights or sunlight, and if any operation is planned, or system of health building is to be adopted, this is the period in which to start these things."
            },
            {
                "period_number": 2,
                "description": "This is a period in which many light and temporary physical conditions may affect the body, and passing emotional conditions affect the mind. In other words, during this period a person may have temporary trouble with the stomach, bowels, bloodstream, and nerves. These conditions seem to come quickly, last but a few days, and pass away quickly. None of these should be neglected; each should be given immediate attention, but there need be no anxiety regarding the continuance of such conditions if immediate attention is given, for all of the influences tend to bring rapid changes in the health and physical condition of the body during these 52 days. During this period there are apt to be days with headaches, upset stomachs, trouble with the eyes or the ears, catarrh, coughs, aches and pains through mild forms of cold, and with women occasionally aches and pains in the breasts and abdomen. During this period everyone should try to be cheerful and not permit the mind to dwell upon the temporary conditions that affect the body, but simply attend promptly to the checking of any condition that may arise and then cast it out of the mind."
            },
            {
                "period_number": 3,
                "description": "This is a period when accidents may happen, and often sudden operations come into one's life, of either a minor or major nature. Likewise, suffering by fire or injury through sharp instruments, falls, or sudden blows, is more likely during this period than any other. Persons should be careful of their food and not overeat, and the body should be kept normally warm because during this period there will be a tendency toward colds, often resulting from overeating or overheating the body. The bloodstream should be kept clean and the bowels active, so that blood conditions will not result in sores, boils, eczema, rashes, or other more serious conditions of the skin and blood. The blood pressure also should be watched during this period, for there will be a tendency for it to rise, and overwork or strain should be avoided. Any abnormal strain upon any part of the body is very apt to bring a breaking down during this period."
            },
            {
                "period_number": 4,
                "description": "During this period the nervous system of your body will be tried to its utmost and there will be many tendencies toward nervousness expressing itself in the functioning of various organs or in an outer form of restlessness and uneasiness. Too much study, reading, planning, or use of the mind and nervous system will surely bring definite reactions during this period. More sleep and more rest are required during this period than in any other part of the year. Fretfulness and nervousness may also affect the digestion, the functioning of the stomach, and may also produce a nervous heart which may cause misgivings and inconvenience. Persons who have been laboring too long or too tediously with mental problems or work requiring mental strain should be forced to relax and rest during this period, or a mental breakdown is inevitable."
            },
            {
                "period_number": 5,
                "description": "This is another good period, when the health should be very good, especially if normal living is indulged in, and the great outdoors utilized for deep breathing, fairly long walks, and good exercise. There will probably be a tendency during this period to overindulge in the things that please the flesh, such as the eating of preferred foods, elaborate meals and banquets, rich concoctions, spicy drinks, and so forth, and even overindulgence morally and ethically in many ways. All of this must be avoided during this period in order to prevent serious conditions. This is a good period in which to recover from fevers, chronic conditions, or other abnormal or subnormal conditions of the body which have been existing for some time. During this period, mental suggestions, metaphysical principles, and right thinking will have more effect upon the body and the health than at any other period."
            },
            {
                "period_number": 6,
                "description": "This period is another one in which overindulgence should be carefully avoided in regard to work, mental strain, eating, or any of the pleasures of the flesh. It is a period during which the skin, throat, internal generative system, and kidneys may become affected. Therefore, plenty of water should be drunk during this period, the bowels kept open, and rest with outdoor exercise should be indulged in more frequently than mental strain or overwork."
            },
            {
                "period_number": 7,
                "description": "This is the period during which chronic or lingering conditions are often contracted, and which remain a long time and cause considerable trouble in overcoming. Everyone should be especially careful of catching colds or contracting serious contagious fevers during this period by avoiding the places where such things may be contacted. The mind and whole nature is very apt to be despondent and below normal in the ability to ward off and fight an incoming condition. Even the bloodstream may be lowered in its vitality at this period and, therefore, is unable to fight even the normal amount of germs or unfavorable influences that generally come in contact with every human being. It is not a good time, however, for taking medicine or having an operation performed, or for starting any new or drastic method of improving the health unless in an emergency or unless it is to be continued over a long period, so that its real effect will come into the next period of 52 days, which will be Period No. 1 of the next cycle. The eyes, the ears, and in fact any one of the five senses may become affected during this period, and care should be taken that colds or other conditions do not linger during this period or continue without proper expert attention. It is one of the most serious periods of the whole year for each person, in regard to diseases and chronic conditions."
            }
        ]

        for period_data in health_cycle_periods:
            CycleTemplate.objects.update_or_create(
                cycle_type='health',
                period_number=period_data['period_number'],
                defaults={'description': period_data['description']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded detailed descriptions for the Health Cycle.'))
