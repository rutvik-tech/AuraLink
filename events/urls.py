from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/checkout/', views.checkout, name='checkout'),
    path('events/<slug:slug>/success/', views.payment_success, name='payment_success'),

    # auth
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # organizer
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/events/create/', views.create_event, name='create_event'),
    path('dashboard/events/<int:pk>/', views.organizer_event_detail, name='organizer_event_detail'),
    path('dashboard/events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('dashboard/events/<int:pk>/delete/', views.delete_event, name='delete_event'),
]
