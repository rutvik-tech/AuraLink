from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Event, Registration, Category
from .forms import RegistrationForm, SignUpForm, EventForm


def home(request):
    # Embedded login handling on homepage (admin login)
    login_form = AuthenticationForm()
    create_form = None
    if request.user.is_authenticated and request.user.is_staff:
        create_form = EventForm()

    # Handle login submission. Accept explicit button press or Enter (username+password present).
    login_attempt = (request.method == 'POST' and (
        request.POST.get('login-submit') or (
            request.POST.get('username') and request.POST.get('password') and not request.POST.get('create-event-submit')
        )
    ))
    if login_attempt:
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            # Let the template display form errors too for clarity
            messages.error(request, 'Login failed — check your username and password.')

    # Handle inline event creation from homepage (staff only)
    if request.method == 'POST' and request.POST.get('create-event-submit'):
        if not (request.user.is_authenticated and request.user.is_staff):
            messages.error(request, 'You are not authorized to create events here.')
            return redirect('home')
        create_form = EventForm(request.POST, request.FILES)
        if create_form.is_valid():
            ev = create_form.save(commit=False)
            ev.organizer = request.user
            ev.save()
            messages.success(request, f'Event "{ev.title}" created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors in the event form.')

    featured = Event.objects.order_by('-start_time')[:6]
    return render(request, 'events/home.html', {'featured': featured, 'login_form': login_form, 'create_form': create_form})


def _can_manage_event(user, event=None):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    if event and hasattr(event, 'organizer') and event.organizer == user:
        return True
    return False


@login_required
def edit_event(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not _can_manage_event(request.user, ev):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=ev)
        if form.is_valid():
            ev = form.save(commit=False)
            if not ev.organizer:
                ev.organizer = request.user
            ev.save()
            messages.success(request, 'Event updated successfully')
            return redirect('organizer_event_detail', pk=ev.pk)
    else:
        form = EventForm(instance=ev)
    return render(request, 'events/event_form.html', {'form': form, 'event': ev})


@login_required
def delete_event(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not _can_manage_event(request.user, ev):
        return HttpResponseForbidden()
    if request.method == 'POST':
        ev.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('dashboard')
    return render(request, 'events/confirm_delete.html', {'event': ev})


def event_list(request):
    # Optional category filter via ?category=<slug>
    category_slug = request.GET.get('category')
    categories = Category.objects.order_by('name')
    qs = Event.objects.order_by('start_time')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        qs = qs.filter(category=selected_category)

    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    context = {
        'events': events,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'events/event_list.html', context)


from django.core.mail import send_mail
from django.conf import settings


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.event = event
            reg.save()

            # send confirmation email (console backend in dev)
            try:
                send_mail(
                    subject=f"Registration confirmed for {event.title}",
                    message=f"Thanks {reg.full_name} for registering for {event.title}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reg.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, 'Registration received — a confirmation email was sent (console in dev).')
            return redirect('event_detail', slug=event.slug)
    else:
        form = RegistrationForm()
    return render(request, 'events/event_detail.html', {'event': event, 'form': form})


def checkout(request, slug):
    """Simple simulated checkout flow (placeholder for Stripe integration)."""
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        # For this demo we treat this as a successful payment and create the registration
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.event = event
            reg.save()
            # send confirmation
            send_mail(
                subject=f"Payment & Registration confirmed for {event.title}",
                message=f"Thanks {reg.full_name} — your payment for {event.title} was received (demo).",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reg.email],
                fail_silently=True,
            )
            return redirect('payment_success', slug=event.slug)
    else:
        form = RegistrationForm()
    return render(request, 'events/checkout.html', {'event': event, 'form': form})


def payment_success(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'events/payment_success.html', {'event': event})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def is_organizer(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_organizer)
def dashboard(request):
    events = Event.objects.filter(organizer=request.user).order_by('-start_time')
    regs = Registration.objects.filter(event__organizer=request.user).order_by('-created_at')[:10]
    stats = {
        'total_events': events.count(),
        'total_registrations': Registration.objects.filter(event__organizer=request.user).count(),
    }
    return render(request, 'events/dashboard.html', {'events': events, 'registrations': regs, 'stats': stats})


@login_required
@user_passes_test(is_organizer)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.organizer = request.user
            ev.save()
            messages.success(request, 'Event created successfully')
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required
@user_passes_test(is_organizer)
def organizer_event_detail(request, pk):
    ev = get_object_or_404(Event, pk=pk, organizer=request.user)
    regs = ev.registrations.all()
    return render(request, 'events/organizer_event_detail.html', {'event': ev, 'registrations': regs})
