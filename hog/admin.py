from django.contrib import admin
from .models import Sermon
from .models import Message

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title',)


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'message', 'date_sent')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('date_sent',)