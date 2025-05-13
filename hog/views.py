from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, EventGallery
from .forms import EventForm, EventGalleryForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

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

@user_passes_test(is_staff, login_url='admin_login')
@login_required(login_url='admin_login')
def admin_dashboard(request):
    events = Event.objects.all().order_by('-year')
    return render(request, 'admin/dashboard.html', {'events': events})

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'admin/login.html')

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
    if request.method == 'POST':
        image = get_object_or_404(EventGallery, id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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