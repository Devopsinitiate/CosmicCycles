
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from .models import UserProfile, Business
from .models import CycleTemplate
from .utils import get_daily_cycle, get_yearly_cycle, get_business_cycle, get_soul_cycle, get_human_life_cycle

class SignUpView(generic.CreateView):
    from .forms import UserRegisterForm
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

from .forms import UserProfileForm, BusinessForm


@login_required
def edit_profile(request):
    """Allow a logged-in user to edit their UserProfile on a separate page."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'cycles/profile_edit.html', {'form': form})


@login_required
def business_list(request):
    """Show a manageable list of the user's businesses with links to create/edit."""
    businesses = Business.objects.filter(user=request.user)
    return render(request, 'cycles/business_list.html', {'businesses': businesses})


@login_required
def business_create(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            biz = form.save(commit=False)
            biz.user = request.user
            biz.save()
            messages.success(request, 'Business added.')
            return redirect('business_list')
    else:
        form = BusinessForm()
    return render(request, 'cycles/business_form.html', {'form': form})


@login_required
def business_edit(request, pk):
    biz = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=biz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business updated.')
            return redirect('business_list')
    else:
        form = BusinessForm(instance=biz)
    return render(request, 'cycles/business_form.html', {'form': form, 'business': biz})


@login_required
def profile_update_api(request):
    """Accept POST from AJAX to update the user's profile and return JSON."""
    if request.method != 'POST':
        return JsonResponse({'error': 'method_not_allowed'}, status=405)
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    form = UserProfileForm(request.POST, instance=user_profile)
    if form.is_valid():
        profile = form.save()
        data = {
            'success': True,
            'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            'business_start_date': profile.business_start_date.isoformat() if profile.business_start_date else None,
            'timezone': profile.timezone,
            'other_dates': profile.other_dates,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def business_delete(request, pk):
    """Delete a user's business via POST (form submit) and redirect back to list."""
    if request.method != 'POST':
        return JsonResponse({'error': 'method_not_allowed'}, status=405)
    biz = get_object_or_404(Business, pk=pk, user=request.user)
    biz.delete()
    messages.success(request, 'Business deleted.')
    return redirect('business_list')


@login_required
def business_delete_api(request, pk):
    """AJAX-friendly delete endpoint returning JSON; preserves same permissions as the standard delete."""
    if request.method != 'POST':
        return JsonResponse({'error': 'method_not_allowed'}, status=405)
    biz = get_object_or_404(Business, pk=pk, user=request.user)
    biz.delete()
    return JsonResponse({'success': True})

@login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        business_form = BusinessForm(request.POST)

        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('dashboard')

        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.user = request.user
            business.save()
            return redirect('dashboard')

    else:
        user_profile_form = UserProfileForm(instance=user_profile)
        business_form = BusinessForm()

    daily_periods, current_daily_period = get_daily_cycle()
    yearly_periods, current_yearly_period, yearly_progress = get_yearly_cycle(user_profile.date_of_birth)
    soul_periods, current_soul_period, soul_progress = get_soul_cycle()
    soul_progress_offset = 283 - (283 * soul_progress / 100)

    human_periods, current_human_period, human_progress = get_human_life_cycle(user_profile.date_of_birth)

    businesses = Business.objects.filter(user=request.user)
    business_cycles = []
    for business in businesses:
        periods, current_period, progress = get_business_cycle(business.establishment_date)
        # try to attach a flattened template for the current business period
        try:
            tpl = CycleTemplate.objects.filter(cycle_type='business', period_number=(periods.index(current_period) + 1) if current_period in periods else None).first() if current_period else None
            if tpl:
                eff = tpl.effects or {}
                tpl_obj = {'description': tpl.description, 'effects': eff, 'start_age': eff.get('start_age'), 'end_age': eff.get('end_age'), 'advice': eff.get('advice') or eff.get('summary')}
            else:
                tpl_obj = None
        except Exception:
            tpl_obj = None

        business_cycles.append({
            'business': {'id': business.id, 'name': business.name},
            'periods': periods,
            'current_period': current_period,
            'progress': progress,
            'template': tpl_obj,
        })

    context = {
        'user_profile_form': user_profile_form,
        'business_form': business_form,
        'user_profile': user_profile,
        'daily_periods': daily_periods,
        'current_daily_period': current_daily_period,
        'yearly_periods': yearly_periods,
        'current_yearly_period': current_yearly_period,
        'yearly_progress': yearly_progress,
        'soul_periods': soul_periods,
        'current_soul_period': current_soul_period,
        'soul_progress': soul_progress,
        'soul_progress_offset': soul_progress_offset,
    'human_periods': human_periods,
    'current_human_period': current_human_period,
    'human_progress': human_progress,
        'businesses': businesses,
        'business_cycles': business_cycles,
    }
    return render(request, 'cycles/dashboard.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    soul_periods, current_soul_period, soul_progress = get_soul_cycle()
    context = {
        'soul_periods': soul_periods,
        'current_soul_period': current_soul_period,
        'soul_progress': soul_progress,
    }
    return render(request, 'cycles/home.html', context)


@login_required
def human_cycle_api(request):
    """Return JSON with human life cycle data for the logged-in user."""
    from .models import UserProfile as _UserProfile
    # Protect against unsaved User() instances in tests - treat as unauthenticated
    if not getattr(request.user, 'is_authenticated', False) or not getattr(request.user, 'pk', None):
        return JsonResponse({'error': 'not_authenticated'}, status=302)
    user_profile = _UserProfile.objects.filter(user=request.user).first()
    if not user_profile or not user_profile.date_of_birth:
        return JsonResponse({'error': 'birth_date_missing'}, status=400)

    periods, current_period, progress = get_human_life_cycle(user_profile.date_of_birth)

    # Determine numeric period number (1-based) for lookup
    period_number = None
    try:
        if isinstance(current_period, dict) and 'name' in current_period:
            # attempt to find index in periods
            for idx, p in enumerate(periods):
                if p is current_period or (p.get('name') == current_period.get('name') and p.get('start_age') == current_period.get('start_age')):
                    period_number = idx + 1
                    break
        elif isinstance(current_period, int):
            period_number = int(current_period)
    except Exception:
        period_number = None

    # Try to include a CycleTemplate for the current human period if available
    template = None
    try:
        if period_number:
            tpl = CycleTemplate.objects.filter(cycle_type='human', period_number=period_number).first()
        else:
            tpl = None

        if tpl:
            # flatten key fields for easier client usage
            tpl_effects = tpl.effects or {}
            template = {
                'description': tpl.description,
                'effects': tpl_effects,
                'start_age': tpl_effects.get('start_age'),
                'end_age': tpl_effects.get('end_age'),
                'advice': tpl_effects.get('advice') or tpl_effects.get('summary')
            }
    except Exception:
        template = None

    data = {
        'periods': periods,
        'current_period': current_period,
        'current_period_number': period_number,
        'progress': progress,
        'template': template,
    }
    return JsonResponse(data)


@login_required
def user_cycle_api(request, cycle_type):
    """Generic endpoint returning cycle periods, current_period, progress and template for a cycle_type."""
    from .models import UserProfile as _UserProfile
    # Protect against unsaved User() instances in tests - treat as unauthenticated
    if not getattr(request.user, 'is_authenticated', False) or not getattr(request.user, 'pk', None):
        return JsonResponse({'error': 'not_authenticated'}, status=302)
    user_profile = _UserProfile.objects.filter(user=request.user).first()
    if cycle_type in ('human',):
        if not user_profile or not user_profile.date_of_birth:
            return JsonResponse({'error': 'birth_date_missing'}, status=400)
        periods, current_period, progress = get_human_life_cycle(user_profile.date_of_birth)
        current_number = None
        try:
            current_number = periods.index(current_period) + 1 if current_period in periods else None
        except Exception:
            current_number = None
    elif cycle_type == 'daily':
        periods, current_period = get_daily_cycle()
        progress = None
        current_number = None
        try:
            current_number = periods.index(current_period) + 1
        except Exception:
            current_number = None
    elif cycle_type == 'yearly':
        if not user_profile or not user_profile.date_of_birth:
            return JsonResponse({'error': 'birth_date_missing'}, status=400)
        periods, current_period, progress = get_yearly_cycle(user_profile.date_of_birth)
        current_number = None
        try:
            current_number = periods.index(current_period) + 1 if current_period in periods else None
        except Exception:
            current_number = None
    elif cycle_type == 'business':
        # for business cycles, optionally return a single business if business_id provided
        business_id = request.GET.get('business_id')
        try:
            businesses_qs = request.user.business_set.all()
        except Exception:
            businesses_qs = []

        if business_id:
            try:
                b = businesses_qs.get(pk=int(business_id))
            except Exception:
                return JsonResponse({'error': 'business_not_found'}, status=404)
            periods, current_period, progress = get_business_cycle(b.establishment_date)
            tpl = CycleTemplate.objects.filter(cycle_type='business', period_number=(periods.index(current_period) + 1) if current_period in periods else None).first() if current_period else None
            # Flatten template effects for client use
            if tpl:
                eff = tpl.effects or {}
                tpl_obj = {'description': tpl.description, 'effects': eff, 'start_age': eff.get('start_age'), 'end_age': eff.get('end_age'), 'advice': eff.get('advice') or eff.get('summary')}
            else:
                tpl_obj = None
            item = {
                'business': {'id': b.id, 'name': b.name},
                'periods': periods,
                'current_period': current_period,
                'progress': progress,
                'template': tpl_obj,
            }
            # Backwards-compat: include legacy 'business' key expected by older clients/tests
            legacy = {'business': b.name, 'periods': periods, 'current_period': current_period, 'progress': progress, 'template': tpl_obj}
            return JsonResponse({'business_cycles': [item], 'business': legacy})

        # otherwise return list for management views
        result = []
        for b in businesses_qs:
            periods, current_period, progress = get_business_cycle(b.establishment_date)
            tpl = CycleTemplate.objects.filter(cycle_type='business', period_number=(periods.index(current_period) + 1) if current_period in periods else None).first() if current_period else None
            if tpl:
                eff = tpl.effects or {}
                tpl_obj = {'description': tpl.description, 'effects': eff, 'start_age': eff.get('start_age'), 'end_age': eff.get('end_age'), 'advice': eff.get('advice') or eff.get('summary')}
            else:
                tpl_obj = None
            result.append({
                'business': {'id': b.id, 'name': b.name},
                'periods': periods,
                'current_period': current_period,
                'progress': progress,
                'template': tpl_obj,
            })
        return JsonResponse({'business_cycles': result})
    elif cycle_type == 'soul':
        # support soul cycle requests
        periods, current_period, progress = get_soul_cycle()
        current_number = None
    else:
        return JsonResponse({'error': 'unsupported_cycle_type'}, status=400)

    # lookup template
    template = None
    try:
        if current_number:
            tpl = CycleTemplate.objects.filter(cycle_type=cycle_type, period_number=current_number).first()
        else:
            tpl = None
        if tpl:
            eff = tpl.effects or {}
            template = {'description': tpl.description, 'effects': eff, 'start_age': eff.get('start_age'), 'end_age': eff.get('end_age'), 'advice': eff.get('advice') or eff.get('summary')}
    except Exception:
        template = None

    return JsonResponse({'periods': periods, 'current_period': current_period, 'current_period_number': current_number, 'progress': progress, 'template': template})
