from django.db import models
from django.utils.text import slugify

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
