from .models import Event, EventCategory, MonthlyEvent
from django.db.models.functions import ExtractYear, ExtractMonth
from calendar import month_name

def monthly_events_processor(request):
    # Get all months for display
    months = [(i, month_name[i]) for i in range(1, 13)]
    
    # Get events grouped by type
    monthly_events = {
        'fellowship_sunday': MonthlyEvent.objects.filter(event_type='Fellowship Sunday'),
        'christmas_carol': MonthlyEvent.objects.filter(event_type='Christmas Carol Competition'),
        'hallelujah_party': MonthlyEvent.objects.filter(event_type='Hallelujah Party'),
        'months': months
    }
    
    return {'monthly_events': monthly_events}

def event_categories(request):
    return {
        'event_categories': EventCategory.objects.all()
    }

def categories_processor(request):
    categories = EventCategory.objects.all()
    events_by_category = {}
    
    for category in categories:
        events_by_category[category.name] = Event.objects.filter(
            category=category
        ).order_by('-year')
    
    return {
        'categories': categories,
        'events_by_category': events_by_category
    }

def events_processor(request):
    return {
        'events_by_category': {
            'Queen_Esther': Event.objects.filter(category__name='Queen Esther').order_by('-year'),
            'GRACE': Event.objects.filter(category__name='G.R.A.C.E').order_by('-year'),
        }
    }

from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        return {
            'unread_count': Message.objects.filter(is_read=False).count()
        }
    return {}