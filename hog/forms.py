from django import forms
from .models import Event, EventGallery, EventCategory

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
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter year'
            }),
            'winner_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter event description'
            })
        }

class EventGalleryForm(forms.ModelForm):
    class Meta:
        model = EventGallery
        fields = ['image', 'caption']