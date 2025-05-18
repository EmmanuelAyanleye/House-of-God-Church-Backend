from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Event Categories"
        
    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    winner_image = models.ImageField(upload_to='events/winners/')
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.year}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category.name} {self.year}"

class EventGallery(models.Model):
    event = models.ForeignKey(Event, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "Event Galleries"

class MonthlyEvent(models.Model):
    EVENT_TYPES = [
        ('Fellowship Sunday', 'Fellowship Sunday'),
        ('Christmas Carol Competition', 'Christmas Carol Competition'),
        ('Hallelujah Party', 'Hallelujah Party'),
    ]
    
    MONTHS = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES)
    month = models.IntegerField(choices=MONTHS, default=1)
    year = models.IntegerField(default=timezone.now().year)
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, default='Main Auditorium')
    description = models.TextField()
    image = models.ImageField(upload_to='monthly_events/', null=True, blank=True)
    coordinator_name = models.CharField(max_length=200, null=True, blank=True)
    coordinator_email = models.EmailField(null=True, blank=True)
    coordinator_image = models.ImageField(upload_to='monthly_events/coordinators/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('event_type', 'month', 'year')
        ordering = ['-year', 'month']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.event_type}-{self.get_month_display()}-{self.year}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_type} - {self.get_month_display()} {self.year}"

class MonthlyEventGallery(models.Model):
    event = models.ForeignKey(MonthlyEvent, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='monthly_events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(default=timezone.now().year)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = 'Monthly Event Galleries'

    def __str__(self):
        return f"Gallery image for {self.event} ({self.year})"

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add

    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.category.name} - {self.date_added.strftime('%Y-%m-%d')}"

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    date_posted = models.DateField(default=timezone.now)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='sermon_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='sermon_dislikes', blank=True)
    
    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()






# contact database
class Message(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # New field
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"
