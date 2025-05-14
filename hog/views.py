from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, EventGallery, MonthlyEvent, MonthlyEventGallery, EventCategory
from .forms import EventForm, EventGalleryForm, MonthlyEventForm, MonthlyEventGalleryForm  # Add this line
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from urllib.parse import unquote
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.utils import timezone
from django.db.models import Max, Count
from django.utils.text import slugify
from calendar import month_name
from itertools import groupby

def index(request):
    return render(request, 'pages/index.html')

def our_church(request):
    return render(request, 'pages/aboutchurch.html')

def our_pastor(request):
    return render(request, 'pages/aboutpastor.html')

def singles(request):
    return render(request, 'pages/singles.html')

def children(request):
    return render(request, 'pages/children.html')

def works(request):
    return render(request, 'pages/works.html')

def publication(request):
    return render(request, 'pages/publication.html')

def evangelism(request):
    return render(request, 'pages/evangelism.html')

def holy(request):
    return render(request, 'pages/holy.html')

def technical(request):
    return render(request, 'pages/technical.html')

def villa(request):
    return render(request, 'pages/villa.html')

def pastoral(request):
    return render(request, 'pages/pastoral.html')

def missions(request):
    return render(request, 'pages/missions.html')

def protocol(request):
    return render(request, 'pages/protocol.html')

def benevolence(request):
    return render(request, 'pages/benevolence.html')

def esther16(request):
    return render(request, 'pages/esther16.html')

def january(request):
    return render(request, 'pages/january.html')

def is_staff(user):
    return user.is_staff

def admin_login(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            # Get the next URL, but sanitize it
            next_url = request.GET.get('next', '')
            if next_url:
                next_url = unquote(next_url)
                # Prevent infinite loops by checking for multiple login occurrences
                if next_url.count('login') > 1:
                    return redirect('admin_dashboard')
            return redirect(next_url or 'admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    events = Event.objects.all()
    monthly_events = MonthlyEvent.objects.annotate(
        gallery_count=Count('gallery')
    ).order_by('-year', 'month')
    
    # Group events by year
    years_data = []
    current_year = None
    year_events = []
    
    for event in monthly_events:
        if current_year != event.year:
            if current_year is not None:
                years_data.append({
                    'event_year': current_year,
                    'events': year_events
                })
            current_year = event.year
            year_events = []
        year_events.append(event)
    
    if year_events:  # Add the last year
        years_data.append({
            'event_year': current_year,
            'events': year_events
        })

    context = {
        'events': events,
        'years': years_data,
    }
    return render(request, 'admin/dashboard.html', context)

def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('admin_login')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        gallery_files = request.FILES.getlist('gallery_images')
        
        if form.is_valid():
            event = form.save()
            
            # Handle multiple gallery images
            for image in gallery_files:
                EventGallery.objects.create(
                    event=event,
                    image=image
                )
            
            messages.success(request, 'Event created successfully!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'admin/event_form.html', {'form': form})

@login_required
def delete_gallery_image(request, image_id):
    # Get the gallery image
    gallery_image = get_object_or_404(MonthlyEventGallery, id=image_id)
    event = gallery_image.event  # Save the event reference before deletion
    
    if request.method == 'POST':
        # Delete the image
        gallery_image.delete()
        messages.success(request, 'Image deleted successfully.')
        
        # Redirect back to the event detail page
        return redirect('monthly_event_detail', slug=event.slug)
    
    # If not POST, redirect back
    return redirect('monthly_event_detail', slug=event.slug)

@login_required
def edit_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            
            # Handle new gallery images
            gallery_files = request.FILES.getlist('gallery_images')
            for image in gallery_files:
                EventGallery.objects.create(
                    event=event,
                    image=image
                )
            
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'admin/event_form.html', {
        'form': form,
        'event': event
    })

@login_required
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    gallery = event.gallery.all()
    return render(request, 'admin/event_detail.html', {
        'event': event,
        'gallery': gallery
    })

@login_required
def add_gallery_images(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.event = event
            gallery.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventGalleryForm()
    return render(request, 'admin/gallery_form.html', {'form': form, 'event': event})

def event_public_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'pages/event_detail.html', {
        'event': event,
        'gallery': event.gallery.all()
    })

def get_event_categories(request):
    queen_esther_events = Event.objects.filter(
        category__name='Queen Esther'
    ).order_by('-year')
    
    grace_events = Event.objects.filter(
        category__name='G.R.A.C.E'
    ).order_by('-year')
    
    return {
        'queen_esther_events': queen_esther_events,
        'grace_events': grace_events
    }

@login_required
def monthly_event_dashboard(request):
    categories = MonthlyEventCategory.objects.all()
    events = MonthlyEvent.objects.all().order_by('-year', 'month')
    return render(request, 'admin/monthly_events/dashboard.html', {
        'categories': categories,
        'events': events
    })

@login_required
def create_monthly_event(request):
    if request.method == 'POST':
        form = MonthlyEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
    else:
        form = MonthlyEventForm()
    return render(request, 'admin/monthly_events/event_form.html', {'form': form})

@login_required
def monthly_event_detail(request, slug):
    event = get_object_or_404(MonthlyEvent, slug=slug)
    
    # Get all galleries and group them by year
    galleries = MonthlyEventGallery.objects.filter(event=event)\
        .order_by('-year', '-date_added')
    
    # Group images by year
    gallery_by_year = []
    for year, images in groupby(galleries, key=lambda x: x.year):
        gallery_by_year.append({
            'grouper': year,
            'list': list(images)
        })
    
    context = {
        'event': event,
        'gallery_by_year': gallery_by_year,
    }
    return render(request, 'admin/monthly_events/event_detail.html', context)

@login_required
def edit_monthly_event(request, pk):
    event = get_object_or_404(MonthlyEvent, pk=pk)
    if request.method == 'POST':
        form = MonthlyEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
    else:
        form = MonthlyEventForm(instance=event)
    return render(request, 'admin/monthly_events/event_form.html', {'form': form, 'event': event})

@login_required
def delete_monthly_event(request, pk):
    event = get_object_or_404(MonthlyEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'admin/monthly_events/confirm_delete.html', {'event': event})

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events_list')
    return render(request, 'admin/events/confirm_delete.html', {'event': event})

@login_required
def events_list(request):
    events = Event.objects.all().order_by('-year')
    categories = EventCategory.objects.all()
    
    # Filter by category if requested
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id
    }
    return render(request, 'admin/events/events_list.html', context)

@login_required
def monthly_events_list(request):
    events = MonthlyEvent.objects.all().order_by('-date')
    
    # Filter by event type if requested
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    context = {
        'events': events,
        'event_types': MonthlyEvent.EVENT_TYPES,
        'selected_type': event_type
    }
    return render(request, 'admin/monthly_events/events_list.html', context)

def monthly_event_public_view(request, category, month, year):
    event = get_object_or_404(MonthlyEvent, 
                            category__name=category,
                            month=month,
                            year=year)
    years = MonthlyEvent.objects.filter(
        category__name=category,
        month=month
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    return render(request, 'pages/monthly_event.html', {
        'event': event,
        'years': years,
        'current_year': year,
        'current_month': month
    })

def monthly_event_month(request, event_type, month):
    event_type_display = event_type.replace('-', ' ').title()
    month_name = dict(MonthlyEvent.MONTHS)[month]
    
    # Get all years that have content for this event type and month
    available_years = MonthlyEvent.objects.filter(
        event_type=event_type_display,
        month=month
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    selected_year = request.GET.get('year')
    gallery = []
    
    if selected_year:
        try:
            event = MonthlyEvent.objects.get(
                event_type=event_type_display,
                month=month,
                year=selected_year
            )
            gallery = event.gallery.all()
        except MonthlyEvent.DoesNotExist:
            pass
    
    context = {
        'event_type': event_type_display,
        'month_name': month_name,
        'available_years': available_years,
        'selected_year': int(selected_year) if selected_year else None,
        'gallery': gallery
    }
    
    template_name = f'monthly_events/{month_name.lower()}.html'
    return render(request, template_name, context)

def monthly_event_view(request, event_type, month):
    # Convert month name to number
    month_names = {m.lower(): i for i, m in enumerate(month_name) if m}
    month_num = month_names.get(month.lower())
    
    if not month_num:
        raise Http404("Month not found")
    
    # Get the current year
    current_year = timezone.now().year
    
    # Get available years for this event/month combination
    years = MonthlyEvent.objects.filter(
        event_type=event_type,
        month=month_num
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    # Default to current year or most recent year if available
    selected_year = request.GET.get('year', years.first() or current_year)
    
    try:
        # Try to get the monthly event
        event = MonthlyEvent.objects.get(
            event_type=event_type,
            month=month_num,
            year=selected_year
        )
        gallery = event.gallery.all().order_by('-date_added')
    except MonthlyEvent.DoesNotExist:
        # If no event exists, provide empty data but render the template
        event = None
        gallery = []
    
    context = {
        'event': event,
        'gallery': gallery,
        'available_years': years,
        'selected_year': int(selected_year),
        'month_name': month_name[month_num],
        'event_type': event_type,
        'no_event': event is None  # Flag to indicate if there's no event
    }
    
    return render(request, 'pages/monthly_event.html', context)

@login_required
def add_monthly_event_gallery(request, event_id):
    event = get_object_or_404(MonthlyEvent, id=event_id)
    initial_year = request.GET.get('year', timezone.now().year)
    
    if request.method == 'POST':
        if not request.FILES.getlist('images'):
            messages.error(request, 'Please select at least one image to upload.')
            return redirect('add_monthly_event_gallery', event_id=event_id)

        year = request.POST.get('year', timezone.now().year)
        files = request.FILES.getlist('images')
        
        created_images = []
        for f in files:
            gallery_image = MonthlyEventGallery.objects.create(
                event=event,
                image=f,
                year=year
            )
            created_images.append(gallery_image)
        
        if created_images:
            messages.success(request, f'{len(created_images)} images uploaded successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
        else:
            messages.error(request, 'No images were uploaded. Please try again.')
    else:
        form = MonthlyEventGalleryForm(initial={'year': initial_year})
    
    context = {
        'form': form,
        'event': event,
        'gallery': event.gallery.all().order_by('-year', '-date_added')
    }
    return render(request, 'admin/monthly_events/add_gallery.html', context)