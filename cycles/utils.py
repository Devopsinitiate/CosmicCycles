from datetime import datetime, timedelta, date


def _ensure_date(d):
    """Accept date, datetime, or ISO date string and return date object."""
    if d is None:
        return None
    if isinstance(d, date) and not isinstance(d, datetime):
        return d
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, str):
        try:
            return datetime.strptime(d, '%Y-%m-%d').date()
        except Exception:
            return None
    return None


def get_daily_cycle(now=None):
    """Return daily periods and the current period based on a 7-part day starting at 6:00 AM.

    Each period is ~3h26m (206 minutes).
    """
    now = now or datetime.now()
    if isinstance(now, date) and not isinstance(now, datetime):
        now = datetime.combine(now, datetime.min.time())
    start_of_day = now.replace(hour=6, minute=0, second=0, microsecond=0)
    start_of_day = now.replace(hour=6, minute=0, second=0, microsecond=0)
    
    if now < start_of_day:
        start_of_day -= timedelta(days=1)

    periods = [
        {"name": "The Morning Period", "start": "6:00 a.m.", "end": "9:26 a.m.", "principle": "New beginnings, planning, and mental work.", "suggestion": "Start new tasks, intellectual work, planning"},
        {"name": "The Active Period", "start": "9:26 a.m.", "end": "12:52 p.m.", "principle": "Action and execution.", "suggestion": "Meetings, negotiations, physical activities"},
        {"name": "The Period of Rest", "start": "12:52 p.m.", "end": "4:18 p.m.", "principle": "Consolidation and rejuvenation.", "suggestion": "Take a break, review work, gather energy"},
        {"name": "The Period of Fulfillment", "start": "4:18 p.m.", "end": "7:44 p.m.", "principle": "The day's efforts begin to bear fruit.", "suggestion": "Complete tasks, prepare for evening"},
        {"name": "The Period of Preparation", "start": "7:44 p.m.", "end": "11:10 p.m.", "principle": "Introspection and preparing for the next day.", "suggestion": "Journaling, creative thinking, planning"},
        {"name": "The Period of Dreams", "start": "11:10 p.m.", "end": "2:36 a.m.", "principle": "Deep rest and subconscious activity.", "suggestion": "Sleep and deep rest"},
        {"name": "The Period of Introspection", "start": "2:36 a.m.", "end": "6:00 a.m.", "principle": "Profound spiritual and creative thought.", "suggestion": "Meditation, deep thinking (if awake)"}
    ]
    
    minutes_since_start = (now - start_of_day).total_seconds() / 60
    period_length = 206  # 3 hours 26 minutes

    current_period_index = int(minutes_since_start // period_length)
    if current_period_index < 0:
        current_period_index = 0
    if current_period_index >= len(periods):
        current_period_index = len(periods) - 1

    return periods, periods[current_period_index]

def get_yearly_cycle(birth_date):
    today = datetime.today().date()
    birth_date = _ensure_date(birth_date)

    if not birth_date:
        return [], None, 0

    try:
        current_year_birthday = birth_date.replace(year=today.year)
    except Exception:
        # handle Feb 29 birthdays on non-leap years
        current_year_birthday = date(today.year, birth_date.month, birth_date.day)

    if today < current_year_birthday:
        cycle_start_date = birth_date.replace(year=today.year - 1)
    else:
        cycle_start_date = current_year_birthday

    days_into_cycle = (today - cycle_start_date).days
    total_days_in_cycle = 365
    progress = (days_into_cycle / total_days_in_cycle) * 100

    periods = [
        {"name": "The Period of Action", "start_day": 1, "end_day": 52, "principle": "Initiate new projects and undertakings.", "suggestion": "Start new projects, set goals, take initiative"},
        {"name": "The Period of Stabilization", "start_day": 53, "end_day": 104, "principle": "Solidify what was started in the first period.", "suggestion": "Focus on consolidation, follow-through, attention to detail"},
        {"name": "The Period of Rejuvenation", "start_day": 105, "end_day": 156, "principle": "Rest, recover, and avoid major new undertakings.", "suggestion": "Lighter schedule, personal wellness activities"},
        {"name": "The Period of Fruition", "start_day": 157, "end_day": 208, "principle": "Reap rewards and success.", "suggestion": "Celebrate successes, reap rewards"},
        {"name": "The Period of Reflection", "start_day": 209, "end_day": 260, "principle": "Review the year and contemplate future goals.", "suggestion": "Review year's progress, contemplate future goals"},
        {"name": "The Period of Transition", "start_day": 261, "end_day": 312, "principle": "Let go of the old and prepare for the new cycle.", "suggestion": "Tie up loose ends, prepare for new cycle"},
        {"name": "The Period of Preparation", "start_day": 313, "end_day": 365, "principle": "Prepare mentally and physically for the new year.", "suggestion": "Make resolutions, get ready for new cycle"}
    ]

    for period in periods:
        period['start_date'] = cycle_start_date + timedelta(days=period['start_day'] - 1)
        period['end_date'] = cycle_start_date + timedelta(days=period['end_day'] - 1)

    current_period = None
    for period in periods:
        if period["start_day"] <= days_into_cycle <= period["end_day"]:
            current_period = period
            break

    return periods, current_period, progress

def get_business_cycle(establishment_date):
    today = datetime.today().date()
    establishment_date = _ensure_date(establishment_date)

    if not establishment_date:
        return [], None, 0

    cycle_start_date = establishment_date
    while cycle_start_date.year < today.year:
        cycle_start_date = cycle_start_date.replace(year=cycle_start_date.year + 1)
    if cycle_start_date > today:
        cycle_start_date = cycle_start_date.replace(year=cycle_start_date.year -1)

    days_since_establishment = (today - establishment_date).days
    days_into_cycle = (days_since_establishment % 365) + 1
    total_days_in_cycle = 365
    progress = (days_into_cycle / total_days_in_cycle) * 100

    periods = [
        {"name": "Action", "start_day": 1, "end_day": 52, "principle": "Launch new products, start marketing campaigns, and expand operations.", "suggestion": "Start marketing campaigns, new initiatives"},
        {"name": "Stabilization", "start_day": 53, "end_day": 104, "principle": "Strengthen business processes, build customer relationships, and improve efficiency.", "suggestion": "Improve efficiency, build customer relationships"},
        {"name": "Rejuvenation", "start_day": 105, "end_day": 156, "principle": "Step back, review the business plan, and prepare for future growth.", "suggestion": "Strategic planning, team-building"},
        {"name": "Fruition", "start_day": 157, "end_day": 208, "principle": "Sales growth, gaining market share, and celebrating business successes.", "suggestion": "Track KPIs, celebrate achievements"},
        {"name": "Reflection", "start_day": 209, "end_day": 260, "principle": "Analyze what worked and what didn't. Time for internal audits and financial review.", "suggestion": "Internal audits, financial review"},
        {"name": "Transition", "start_day": 261, "end_day": 312, "principle": "Prepare the business for the next cycle. Close out old projects or restructure teams.", "suggestion": "Close old projects, restructure"},
        {"name": "Preparation", "start_day": 313, "end_day": 365, "principle": "Fine-tune strategies and prepare for the next year's major initiatives.", "suggestion": "Plan for next year's initiatives"}
    ]

    for period in periods:
        period['start_date'] = cycle_start_date + timedelta(days=period['start_day'] - 1)
        period['end_date'] = cycle_start_date + timedelta(days=period['end_day'] - 1)

    current_period = None
    for period in periods:
        if period["start_day"] <= days_into_cycle <= period["end_day"]:
            current_period = period
            break

    return periods, current_period, progress

def get_soul_cycle():
    today = datetime.today()
    
    periods = [
        {"name": "The Period of Self-Realization", "start_date": (3, 22), "end_date": (5, 12), "principle": "Personal growth, creativity, and the development of new ideas.", "suggestion": "Develop new ideas, focus on personal development"},
        {"name": "The Period of Integration", "start_date": (5, 13), "end_date": (7, 3), "principle": "Integrate new ideas and inspirations into daily life.", "suggestion": "Put plans into action, apply new skills"},
        {"name": "The Period of Consolidation", "start_date": (7, 4), "end_date": (8, 24), "principle": "Solidify relationships and professional connections.", "suggestion": "Network, strengthen professional connections"},
        {"name": "The Period of Release", "start_date": (8, 25), "end_date": (10, 15), "principle": "Let go of old habits and negative influences.", "suggestion": "Self-reflection, break bad habits"},
        {"name": "The Period of Regeneration", "start_date": (10, 16), "end_date": (12, 5), "principle": "Spiritual growth and renewal.", "suggestion": "Introspection, personal development"},
        {"name": "The Period of Harmony", "start_date": (12, 6), "end_date": (1, 25), "principle": "Finding balance in all aspects of life.", "suggestion": "Work-life balance, stress management"},
        {"name": "The Period of Preparation", "start_date": (1, 26), "end_date": (3, 21), "principle": "Prepare for new beginnings and spiritual growth.", "suggestion": "Planning, goal-setting for new year"}
    ]

    for period in periods:
        start_month, start_day = period["start_date"]
        end_month, end_day = period["end_date"]
        year = today.year
        start_date = date(year, start_month, start_day)
        end_date = date(year, end_month, end_day)
        if start_date > end_date:
            if today.month < start_month:
                start_date = start_date.replace(year=year-1)
            else:
                end_date = end_date.replace(year=year+1)
        period['start_date'] = start_date
        period['end_date'] = end_date

    current_period = None
    for period in periods:
        if period["start_date"] <= today.date() <= period["end_date"]:
            current_period = period
            break
    
    total_days_in_year = 365.25
    start_of_soul_cycle = datetime(today.year, 3, 22)
    if today < start_of_soul_cycle:
        start_of_soul_cycle = datetime(today.year - 1, 3, 22)
    
    days_into_cycle = (today - start_of_soul_cycle).days
    progress = (days_into_cycle / total_days_in_year) * 100


    return periods, current_period, progress


def get_human_life_cycle(birth_date):
    """Compute the human life 7-period cycle (approx 144 years divided by 7-year periods).

    Returns periods list and the current period index and progress within that period.
    """
    birth_date = _ensure_date(birth_date)
    today = datetime.today().date()

    if not birth_date:
        return [], None, 0

    total_years = 144
    period_years = 7
    total_periods = total_years // period_years

    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age_years < 0:
        age_years = 0

    current_period_index = min(age_years // period_years, total_periods - 1)
    years_into_period = age_years % period_years
    progress = (years_into_period / period_years) * 100

    periods = []
    for i in range(total_periods):
        start_age = i * period_years
        end_age = start_age + period_years - 1
        start_date = birth_date.replace(year=birth_date.year + start_age)
        end_date = birth_date.replace(year=birth_date.year + end_age)
        periods.append({
            'name': f'Period {i+1}',
            'start_age': start_age,
            'end_age': end_age,
            'start_date': start_date,
            'end_date': end_date,
            'principle': '',
            'suggestion': ''
        })

    current_period = periods[current_period_index]
    return periods, current_period, progress

def get_health_cycle(birth_date):
    today = datetime.today().date()
    birth_date = _ensure_date(birth_date)

    if not birth_date:
        return [], None, 0

    try:
        current_year_birthday = birth_date.replace(year=today.year)
    except Exception:
        # handle Feb 29 birthdays on non-leap years
        current_year_birthday = date(today.year, birth_date.month, birth_date.day)

    if today < current_year_birthday:
        cycle_start_date = birth_date.replace(year=today.year - 1)
    else:
        cycle_start_date = current_year_birthday

    days_into_cycle = (today - cycle_start_date).days
    total_days_in_cycle = 365
    progress = (days_into_cycle / total_days_in_cycle) * 100

    periods = [
        {"name": "Period 1", "start_day": 1, "end_day": 52, "principle": "Vitality and constitutional health at its best.", "suggestion": "During this period the vitality and constitutional health should be at its best and, if it is below normal, it will be more quickly and easily increased and strengthened by normal living and the avoidance of the violation of any natural laws. Plenty of outdoor walking, good air, drinking plenty of water and eating proper foods, avoiding foods that are overheating, especially the starches and raw or rare meats—this will yield results. The eyes should be guarded against overuse or use in bright electric lights or sunlight, and if any operation is planned, or system of health building is to be adopted, this is the period in which to start these things."},
        {"name": "Period 2", "start_day": 53, "end_day": 104, "principle": "Light and temporary physical conditions may affect the body.", "suggestion": "This is a period in which many light and temporary physical conditions may affect the body, and passing emotional conditions affect the mind. In other words, during this period a person may have temporary trouble with the stomach, bowels, bloodstream, and nerves. These conditions seem to come quickly, last but a few days, and pass away quickly. None of these should be neglected; each should be given immediate attention, but there need be no anxiety regarding the continuance of such conditions if immediate attention is given, for all of the influences tend to bring rapid changes in the health and physical condition of the body during these 52 days. During this period there are apt to be days with headaches, upset stomachs, trouble with the eyes or the ears, catarrh, coughs, aches and pains through mild forms of cold, and with women occasionally aches and pains in the breasts and abdomen. During this period everyone should try to be cheerful and not permit the mind to dwell upon the temporary conditions that affect the body, but simply attend promptly to the checking of any condition that may arise and then cast it out of the mind."},
        {"name": "Period 3", "start_day": 105, "end_day": 156, "principle": "Accidents may happen, and often sudden operations come into one's life.", "suggestion": "This is a period when accidents may happen, and often sudden operations come into one’s life, of either a minor or major nature. Likewise, suffering by fire or injury through sharp instruments, falls, or sudden blows, is more likely during this period than any other. Persons should be careful of their food and not overeat, and the body should be kept normally warm because during this period there will be a tendency toward colds, often resulting from overeating or overheating the body. The bloodstream should be kept clean and the bowels active, so that blood conditions will not result in sores, boils, eczema, rashes, or other more serious conditions of the skin and blood. The blood pressure also should be watched during this period, for there will be a tendency for it to rise, and overwork or strain should be avoided. Any abnormal strain upon any part of the body is very apt to bring a breaking down during this period."},
        {"name": "Period 4", "start_day": 157, "end_day": 208, "principle": "The nervous system of your body will be tried to its utmost.", "suggestion": "During this period the nervous system of your body will be tried to its utmost and there will be many tendencies toward nervousness expressing itself in the functioning of various organs or in an outer form of restlessness and uneasiness. Too much study, reading, planning, or use of the mind and nervous system will surely bring definite reactions during this period. More sleep and more rest are required during this period than in any other part of the year. Fretfulness and nervousness may also affect the digestion, the functioning of the stomach, and may also produce a nervous heart which may cause misgivings and inconvenience. Persons who have been laboring too long or too tediously with mental problems or work requiring mental strain should be forced to relax and rest during this period, or a mental breakdown is inevitable."},
        {"name": "Period 5", "start_day": 209, "end_day": 260, "principle": "Health should be very good, especially if normal living is indulged in.", "suggestion": "This is another good period, when the health should be very good, especially if normal living is indulged in, and the great outdoors utilized for deep breathing, fairly long walks, and good exercise. There will probably be a tendency during this period to overindulge in the things that please the flesh, such as the eating of preferred foods, elaborate meals and banquets, rich concoctions, spicy drinks, and so forth, and even overindulgence morally and ethically in many ways. All of this must be avoided during this period in order to prevent serious conditions. This is a good period in which to recover from fevers, chronic conditions, or other abnormal or subnormal conditions of the body which have been existing for some time. During this period, mental suggestions, metaphysical principles, and right thinking will have more effect upon the body and the health than at any other period."},
        {"name": "Period 6", "start_day": 261, "end_day": 312, "principle": "Overindulgence should be carefully avoided in regard to work, mental strain, eating, or any of the pleasures of the flesh.", "suggestion": "This period is another one in which overindulgence should be carefully avoided in regard to work, mental strain, eating, or any of the pleasures of the flesh. It is a period during which the skin, throat, internal generative system, and kidneys may become affected. Therefore, plenty of water should be drunk during this period, the bowels kept open, and rest with outdoor exercise should be indulged in more frequently than mental strain or overwork."},
        {"name": "Period 7", "start_day": 313, "end_day": 365, "principle": "Chronic or lingering conditions are often contracted.", "suggestion": "This is the period during which chronic or lingering conditions are often contracted, and which remain a long time and cause considerable trouble in overcoming. Everyone should be especially careful of catching colds or contracting serious contagious fevers during this period by avoiding the places where such things may be contacted. The mind and whole nature is very apt to be despondent and below normal in the ability to ward off and fight an incoming condition. Even the bloodstream may be lowered in its vitality at this period and, therefore, is unable to fight even the normal amount of germs or unfavorable influences that generally come in contact with every human being. It is not a good time, however, for taking medicine or having an operation performed, or for starting any new or drastic method of improving the health unless in an emergency or unless it is to be continued over a long period, so that its real effect will come into the next period of 52 days, which will be Period No. 1 of the next cycle. The eyes, the ears, and in fact any one of the five senses may become affected during this period, and care should be taken that colds or other conditions do not linger during this period or continue without proper expert attention. It is one of the most serious periods of the whole year for each person, in regard to diseases and chronic conditions."}
    ]

    for period in periods:
        period['start_date'] = cycle_start_date + timedelta(days=period['start_day'] - 1)
        period['end_date'] = cycle_start_date + timedelta(days=period['end_day'] - 1)

    current_period = None
    for period in periods:
        if period["start_day"] <= days_into_cycle <= period["end_day"]:
            current_period = period
            break

    return periods, current_period, progress

def get_reincarnation_cycle(birth_date):
    today = datetime.today().date()
    birth_date = _ensure_date(birth_date)

    if not birth_date:
        return [], None, 0

    total_years = 144
    years_in_cycle = 12 
    cycles_in_lifetime = total_years // years_in_cycle

    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age_years < 0:
        age_years = 0

    current_cycle_index = min(age_years // years_in_cycle, cycles_in_lifetime - 1)
    years_into_cycle = age_years % years_in_cycle
    progress = (years_into_cycle / years_in_cycle) * 100

    periods = [
        {"name": "Cycle 1 (Ages 0-11)", "start_age": 0, "end_age": 11, "principle": "Childhood and the soul's descent into the body. The personality is latent.", "suggestion": "Focus on nurturing and providing a stable environment for the soul's incarnation."},
        {"name": "Cycle 2 (Ages 12-23)", "start_age": 12, "end_age": 23, "principle": "Adolescence and the awakening of personality. The ego begins to assert itself.", "suggestion": "Guide the development of a healthy ego and sense of self."},
        {"name": "Cycle 3 (Ages 24-35)", "start_age": 24, "end_age": 35, "principle": "Early adulthood and the soul's struggle for expression. The personality is dominant.", "suggestion": "Encourage the individual to find their true calling and purpose."},
        {"name": "Cycle 4 (Ages 36-47)", "start_age": 36, "end_age": 47, "principle": "Maturity and the soul's search for meaning. The personality begins to yield to the soul.", "suggestion": "Support the individual in their quest for spiritual understanding."},
        {"name": "Cycle 5 (Ages 48-59)", "start_age": 48, "end_age": 59, "principle": "Mid-life and the soul's illumination. The personality is now a vehicle for the soul.", "suggestion": "Assist the individual in sharing their wisdom and experience with others."},
        {"name": "Cycle 6 (Ages 60-71)", "start_age": 60, "end_age": 71, "principle": "Later life and the soul's detachment from the physical world. The personality is transcended.", "suggestion": "Help the individual prepare for the transition from the physical to the spiritual realm."},
        {"name": "Cycle 7 (Ages 72-83)", "start_age": 72, "end_age": 83, "principle": "Old age and the soul's return to its source. The personality is dissolved.", "suggestion": "Provide comfort and support as the individual completes their earthly journey."},
        {"name": "Cycle 8 (Ages 84-95)", "start_age": 84, "end_age": 95, "principle": "The soul's journey through the spiritual worlds. The personality is a distant memory.", "suggestion": "This is a time of cosmic consciousness and unity with the Divine."},
        {"name": "Cycle 9 (Ages 96-107)", "start_age": 96, "end_age": 107, "principle": "The soul's assimilation of its earthly experiences. The personality is completely absorbed.", "suggestion": "The soul prepares for its next incarnation."},
        {"name": "Cycle 10 (Ages 108-119)", "start_age": 108, "end_age": 119, "principle": "The soul's choice of a new destiny. The personality is a seed of future potential.", "suggestion": "The soul selects the time, place, and circumstances of its next birth."},
        {"name": "Cycle 11 (Ages 120-131)", "start_age": 120, "end_age": 131, "principle": "The soul's preparation for rebirth. The personality is a blueprint for the new life.", "suggestion": "The soul awaits the moment of its return to the physical world."},
        {"name": "Cycle 12 (Ages 132-143)", "start_age": 132, "end_age": 143, "principle": "The soul's descent into a new body. The personality is a fresh canvas.", "suggestion": "A new life begins, and the cycle of reincarnation continues."}
    ]

    for period in periods:
        period['start_date'] = birth_date.replace(year=birth_date.year + period['start_age'])
        period['end_date'] = birth_date.replace(year=birth_date.year + period['end_age'])

    current_period = periods[current_cycle_index]
    return periods, current_period, progress
