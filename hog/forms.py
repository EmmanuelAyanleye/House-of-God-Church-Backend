from django import forms
from django.utils import timezone
from .models import Event, EventGallery, EventCategory, MonthlyEvent, MonthlyEventGallery, Sermon
from .widgets import MultipleFileInput

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    class Meta:
        model = Event
        fields = ['category', 'title', 'year', 'winner_image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'winner_image': forms.FileInput(attrs={'class': 'form-control'})
        }

class EventGalleryForm(forms.ModelForm):
    class Meta:
        model = EventGallery
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'})
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MonthlyEventForm(forms.ModelForm):
    class Meta:
        model = MonthlyEvent
        fields = [
            'title', 'event_type', 'month', 'year', 'date', 'location',
            'description', 'image', 'coordinator_name', 'coordinator_email',
            'coordinator_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 1000,
                'oninput': 'updateCharCount(this)'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'coordinator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'coordinator_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'coordinator_image': forms.FileInput(attrs={'class': 'form-control'})
        }

class MonthlyEventGalleryForm(forms.Form):
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=timezone.now().year
    )

class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = ['youtube_url', 'title', 'date_posted', 'description']