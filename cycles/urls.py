
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.profile_update_api, name='profile_update_api'),
    path('businesses/', views.business_list, name='business_list'),
    path('businesses/add/', views.business_create, name='business_create'),
    path('businesses/<int:pk>/edit/', views.business_edit, name='business_edit'),
    path('businesses/<int:pk>/delete/', views.business_delete, name='business_delete'),
    path('businesses/<int:pk>/delete/json/', views.business_delete_api, name='business_delete_api'),
    path('api/user_cycle/human/', views.human_cycle_api, name='human_cycle_api'),
    path('api/user_cycle/<str:cycle_type>/', views.user_cycle_api, name='user_cycle_api'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
