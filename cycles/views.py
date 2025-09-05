
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from .models import UserProfile, Business
from .models import CycleTemplate
from .utils import get_daily_cycle, get_yearly_cycle, get_business_cycle, get_soul_cycle, get_human_life_cycle, get_health_cycle, get_reincarnation_cycle

def _get_template_for_cycle(cycle_type, period_number):
    """Helper function to get the template for a given cycle type and period number."""
    try:
        tpl = CycleTemplate.objects.get(cycle_type=cycle_type, period_number=period_number)
        return {
            'description': tpl.description,
            'effects': tpl.effects or {},
            'start_age': (tpl.effects or {}).get('start_age'),
            'end_age': (tpl.effects or {}).get('end_age'),
            'advice': (tpl.effects or {}).get('advice') or (tpl.effects or {}).get('summary'),
            'full_description': tpl.description
        }
    except CycleTemplate.DoesNotExist:
        return None

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
    health_periods, current_health_period, health_progress = get_health_cycle(user_profile.date_of_birth)
    reincarnation_periods, current_reincarnation_period, reincarnation_progress = get_reincarnation_cycle(user_profile.date_of_birth)

    # Get full descriptions for all periods
    for period in yearly_periods:
        try:
            template = CycleTemplate.objects.get(cycle_type='yearly', period_number=yearly_periods.index(period) + 1)
            period['full_description'] = template.description
        except (CycleTemplate.DoesNotExist, ValueError, AttributeError):
            period['full_description'] = ''

    for period in soul_periods:
        try:
            template = CycleTemplate.objects.get(cycle_type='soul', period_number=soul_periods.index(period) + 1)
            period['full_description'] = template.description
        except (CycleTemplate.DoesNotExist, ValueError, AttributeError):
            period['full_description'] = ''

    for period in health_periods:
        try:
            template = CycleTemplate.objects.get(cycle_type='health', period_number=health_periods.index(period) + 1)
            period['full_description'] = template.description
        except (CycleTemplate.DoesNotExist, ValueError, AttributeError):
            period['full_description'] = ''

    for period in reincarnation_periods:
        try:
            template = CycleTemplate.objects.get(cycle_type='reincarnation', period_number=reincarnation_periods.index(period) + 1)
            period['full_description'] = template.description
        except (CycleTemplate.DoesNotExist, ValueError, AttributeError):
            period['full_description'] = ''

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
            'full_description': tpl.description if tpl else ''
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
        'health_periods': health_periods,
        'current_health_period': current_health_period,
        'health_progress': health_progress,
        'reincarnation_periods': reincarnation_periods,
        'current_reincarnation_period': current_reincarnation_period,
        'reincarnation_progress': reincarnation_progress,
    }
    return render(request, 'cycles/dashboard.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    daily_periods, current_daily_period = get_daily_cycle()
    context = {
        'daily_periods': daily_periods,
        'current_daily_period': current_daily_period,
    }
    return render(request, 'cycles/home.html', context)

def about(request):
    return render(request, 'cycles/about.html')








@login_required
def user_cycle_api(request, cycle_type):
    """Generic endpoint returning cycle periods, current_period, progress and template for a cycle_type."""
    from .models import UserProfile as _UserProfile
    # Protect against unsaved User() instances in tests - treat as unauthenticated
    if not getattr(request.user, 'is_authenticated', False) or not getattr(request.user, 'pk', None):
        return JsonResponse({'error': 'not_authenticated'}, status=302)
    user_profile = _UserProfile.objects.filter(user=request.user).first()

    periods, current_period, progress = None, None, None
    current_number = None

    if cycle_type in ('human', 'yearly', 'health', 'reincarnation'):
        if not user_profile or not user_profile.date_of_birth:
            return JsonResponse({'error': 'birth_date_missing'}, status=400)
        if cycle_type == 'human':
            periods, current_period, progress = get_human_life_cycle(user_profile.date_of_birth)
        elif cycle_type == 'yearly':
            periods, current_period, progress = get_yearly_cycle(user_profile.date_of_birth)
        elif cycle_type == 'health':
            periods, current_period, progress = get_health_cycle(user_profile.date_of_birth)
        elif cycle_type == 'reincarnation':
            periods, current_period, progress = get_reincarnation_cycle(user_profile.date_of_birth)
        try:
            current_number = periods.index(current_period) + 1 if current_period in periods else None
        except (ValueError, AttributeError):
            current_number = None

    elif cycle_type == 'daily':
        periods, current_period = get_daily_cycle()
        try:
            current_number = periods.index(current_period) + 1
        except (ValueError, AttributeError):
            current_number = None

    elif cycle_type == 'soul':
        periods, current_period, progress = get_soul_cycle()
        try:
            current_number = periods.index(current_period) + 1 if current_period in periods else None
        except (ValueError, AttributeError):
            current_number = None

    elif cycle_type == 'business':
        business_id = request.GET.get('business_id')
        try:
            businesses_qs = request.user.business_set.all()
        except Exception:
            businesses_qs = []

        if business_id:
            try:
                b = businesses_qs.get(pk=int(business_id))
                periods, current_period, progress = get_business_cycle(b.establishment_date)
                current_number = periods.index(current_period) + 1 if current_period in periods else None
                template = _get_template_for_cycle(cycle_type, current_number)
                item = {
                    'business': {'id': b.id, 'name': b.name},
                    'periods': periods,
                    'current_period': current_period,
                    'progress': progress,
                    'template': template,
                }
                legacy = {'business': b.name, 'periods': periods, 'current_period': current_period, 'progress': progress, 'template': template}
                return JsonResponse({'business_cycles': [item], 'business': legacy})
            except Exception:
                return JsonResponse({'error': 'business_not_found'}, status=404)
        else:
            result = []
            for b in businesses_qs:
                periods, current_period, progress = get_business_cycle(b.establishment_date)
                current_number = periods.index(current_period) + 1 if current_period in periods else None
                template = _get_template_for_cycle(cycle_type, current_number)
                result.append({
                    'business': {'id': b.id, 'name': b.name},
                    'periods': periods,
                    'current_period': current_period,
                    'progress': progress,
                    'template': template,
                })
            return JsonResponse({'business_cycles': result})

    else:
        return JsonResponse({'error': 'unsupported_cycle_type'}, status=400)

    template = _get_template_for_cycle(cycle_type, current_number)

    return JsonResponse({'periods': periods, 'current_period': current_period, 'current_period_number': current_number, 'progress': progress, 'template': template})

