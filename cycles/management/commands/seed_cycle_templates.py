from django.core.management.base import BaseCommand
from cycles.models import CycleTemplate

class Command(BaseCommand):
    help = 'Seed CycleTemplate entries with basic descriptions'

    def handle(self, *args, **options):
        # Structured placeholder templates (non-copyright summaries)
        templates = [
            # Human life cycles: 7-year-ish periods (common system uses 12 periods as example)
            # Paraphrased human period descriptions (book-aligned, reworded for brevity)
            ('human', 1, 'Inception & Foundations', {
                'summary': 'A phase of dependence where basic patterns, trust and attachment form.',
                'advice': 'Provide steady care, consistent routines and nurturing environments.',
                'start_age': 0, 'end_age': 6,
                'effects': ['Rapid physical and sensory development', 'Primary bonding and trust formation']
            }),
            ('human', 2, 'Exploration & Skill Building', {
                'summary': 'Curiosity and early learning expand physical and social abilities.',
                'advice': 'Encourage play-based learning, language, and social skills.',
                'start_age': 7, 'end_age': 13,
                'effects': ['Language and motor skill growth', 'Social interaction patterns emerge']
            }),
            ('human', 3, 'Identity & Apprenticeship', {
                'summary': 'Forming personal identity and beginning serious learning or training.',
                'advice': 'Support mentorship, education and responsible risk-taking.',
                'start_age': 14, 'end_age': 20,
                'effects': ['Self-definition', 'Educational focus and skill acquisition']
            }),
            ('human', 4, 'Initiation & Independence', {
                'summary': 'Establishing independence, early career moves and intimate bonds.',
                'advice': 'Prioritise skill application, relationship-building and steady routines.',
                'start_age': 21, 'end_age': 27,
                'effects': ['Career starts', 'Forming long-term partnerships']
            }),
            ('human', 5, 'Consolidation & Responsibility', {
                'summary': 'Growth into stable roles, responsibility and longer-term planning.',
                'advice': 'Balance commitments, save, and build reliable systems.',
                'start_age': 28, 'end_age': 34,
                'effects': ['Financial and familial responsibilities', 'Career development']
            }),
            ('human', 6, 'Reassessment & Reorientation', {
                'summary': 'A turning point for reassessment, possible change and renewed learning.',
                'advice': 'Reflect on priorities, invest in health and broaden skills.',
                'start_age': 35, 'end_age': 41,
                'effects': ['Career transitions', 'Shifting life priorities']
            }),
            ('human', 7, 'Authority & Mentorship', {
                'summary': 'Leadership, mastery and passing on knowledge to others.',
                'advice': 'Share expertise, mentor younger people and solidify legacy work.',
                'start_age': 42, 'end_age': 48,
                'effects': ['Leadership roles', 'Mentoring responsibilities']
            }),
            ('human', 8, 'Perspective & Stewardship', {
                'summary': 'Broader perspective on life priorities and preparing transitions.',
                'advice': 'Plan succession, balance legacy goals with personal wellbeing.',
                'start_age': 49, 'end_age': 55,
                'effects': ['Strategic thinking', 'Succession planning']
            }),
            ('human', 9, 'Harvest & Sharing', {
                'summary': 'Reaping rewards of earlier efforts and increased community focus.',
                'advice': 'Share knowledge, invest in community ties and mentorship.',
                'start_age': 56, 'end_age': 62,
                'effects': ['Community engagement', 'Mentorship and wisdom-sharing']
            }),
            ('human', 10, 'Reflection & Wellbeing', {
                'summary': 'Slower pace, emphasis on wellbeing and reflection on accomplishments.',
                'advice': 'Prioritise health, close meaningful projects and enjoy family time.',
                'start_age': 63, 'end_age': 69,
                'effects': ['Reflection', 'Health-focused routines']
            }),
            ('human', 11, 'Inward Work & Legacy', {
                'summary': 'Turning inward to reconcile life lessons and preserve memories.',
                'advice': 'Document wisdom, nurture relationships and settle practical matters.',
                'start_age': 70, 'end_age': 76,
                'effects': ['Spiritual integration', 'Archivist and legacy activities']
            }),
            ('human', 12, 'Completion & Handover', {
                'summary': 'A time of completion, handing over roles and final priorities.',
                'advice': 'Ensure affairs are in order and support carers and successors.',
                'start_age': 77, 'end_age': 99,
                'effects': ['Finalisation', 'Generational handover']
            }),

            # Yearly cycle paraphrases
            ('yearly', 1, 'Initiation (Year)', {
                'summary': 'A phase for new goals and setting direction for the year.',
                'advice': 'Set priorities and outline achievable milestones.'
            }),
            ('yearly', 2, 'Execution (Year)', {
                'summary': 'Period focused on carrying out plans and refining efforts.',
                'advice': 'Monitor progress and adjust tactics as needed.'
            }),

            # Daily cycle paraphrases
            ('daily', 1, 'Morning', {
                'summary': 'Highest clarity and planning potential; start important tasks here.',
                'advice': 'Schedule mental work and planning sessions.',
                'effects': ['High focus', 'Good planning capacity']
            }),
            ('daily', 2, 'Afternoon', {
                'summary': 'Sustained energy for execution and collaboration.',
                'advice': 'Use for meetings, implementation and steady effort.',
                'effects': ['Task completion', 'Collaborative work']
            }),
            ('daily', 3, 'Evening', {
                'summary': 'Winding down; review and creative reflection.',
                'advice': 'Review progress and handle low-effort creative tasks.',
                'effects': ['Reflection', 'Creative exploration']
            }),

            # Business cycle paraphrases (7-part business year mapping)
            ('business', 1, 'Launch Phase', {
                'summary': 'Initiate offerings, test the market and gain early traction.',
                'advice': 'Focus on MVP, customer feedback, and quick iterations.',
                'effects': ['Product testing', 'Early customer discovery']
            }),
            ('business', 2, 'Stabilization', {
                'summary': 'Strengthen operations and customer relationships.',
                'advice': 'Improve processes and prioritize customer retention.',
                'effects': ['Process improvement', 'Customer support emphasis']
            }),
            ('business', 3, 'Optimization', {
                'summary': 'Refine offerings and optimise cost and delivery.',
                'advice': 'Streamline operations and iterate on product-market fit.',
                'effects': ['Efficiency gains', 'Refined product-market fit']
            }),
            ('business', 4, 'Growth', {
                'summary': 'Scale successful initiatives and expand reach.',
                'advice': 'Invest in marketing and scalable infrastructure.',
                'effects': ['Revenue growth', 'Scaling challenges']
            }),
            ('business', 5, 'Maturity', {
                'summary': 'Stable operations with predictable cashflow and market position.',
                'advice': 'Consolidate strengths and protect market share.',
                'effects': ['Stable revenues', 'Brand solidity']
            }),
            ('business', 6, 'Renewal', {
                'summary': 'Reassess strategy, pivot if necessary, and invest in renewal.',
                'advice': 'Explore new offerings and invest in people development.',
                'effects': ['Strategic pivots', 'Investment in talent']
            }),
            ('business', 7, 'Succession & Legacy', {
                'summary': 'Prepare leadership transitions and long-term handover plans.',
                'advice': 'Document processes and plan succession carefully.',
                'effects': ['Legacy planning', 'Succession readiness']
            }),
            # Soul cycle paraphrases (larger spiritual/inner cycles)
            ('soul', 1, 'Awakening & Calling', {
                'summary': 'An emergence of deeper purpose and the first stirrings of a soul-level calling.',
                'advice': 'Listen to inner nudges, begin spiritual practices and journal impressions.',
                'effects': ['Heightened intuition', 'Sense of mission']
            }),
            ('soul', 2, 'Formation & Discipline', {
                'summary': 'A period of forming practices, discipline and grounding spiritual work.',
                'advice': 'Establish routines, study spiritual teachings and seek mentors.',
                'effects': ['Practice formation', 'Steady growth']
            }),
            ('soul', 3, 'Service & Expression', {
                'summary': 'Expressing inner gifts outwardly through service, teaching or creative work.',
                'advice': 'Find ways to contribute talents; balance service with self-care.',
                'effects': ['Community service', 'Creative expression']
            }),
            ('soul', 4, 'Trial & Purification', {
                'summary': 'Challenges that clear disruptions and deepen spiritual maturity.',
                'advice': 'Face difficulties with compassion and seek cleansing practices.',
                'effects': ['Inner resilience', 'Clarified priorities']
            }),
            ('soul', 5, 'Integration & Wisdom', {
                'summary': 'Synthesis of lessons and a mature, steady orientation of the soul.',
                'advice': 'Teach, write, or embody what you have learned.',
                'effects': ['Embodied wisdom', 'Mentoring others']
            }),
        ]

        created = 0
        for t in templates:
            # template tuples are inconsistent to allow quick additions; normalize
            cycle_type = t[0]
            period_number = t[1]
            description = t[2] if len(t) > 2 else ''
            effects = t[3] if len(t) > 3 else {}
            obj, _ = CycleTemplate.objects.update_or_create(
                cycle_type=cycle_type, period_number=period_number,
                defaults={'description': description, 'effects': effects}
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created/Updated {created} CycleTemplate entries'))
