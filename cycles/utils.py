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

    current_period = None
    for period in periods:
        start_month, start_day = period["start_date"]
        end_month, end_day = period["end_date"]

        if start_month > end_month: # Wraps around the new year
            if (today.month >= start_month and today.day >= start_day) or \
               (today.month <= end_month and today.day <= end_day):
                current_period = period
                break
        else:
            if (start_month <= today.month <= end_month) and \
               (start_day <= today.day if today.month == start_month else True) and \
               (today.day <= end_day if today.month == end_month else True):
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
        periods.append({
            'name': f'Period {i+1}',
            'start_age': start_age,
            'end_age': end_age,
            'principle': '',
            'suggestion': ''
        })

    current_period = periods[current_period_index]
    return periods, current_period, progress
