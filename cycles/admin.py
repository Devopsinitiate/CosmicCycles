from django.contrib import admin
from .models import UserProfile, Business, CycleTemplate, UserCycle


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'date_of_birth', 'timezone')


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'establishment_date')


@admin.register(CycleTemplate)
class CycleTemplateAdmin(admin.ModelAdmin):
	list_display = ('cycle_type', 'period_number')
	list_filter = ('cycle_type',)


@admin.register(UserCycle)
class UserCycleAdmin(admin.ModelAdmin):
	list_display = ('user_profile', 'cycle_type', 'start_date', 'current_period')
