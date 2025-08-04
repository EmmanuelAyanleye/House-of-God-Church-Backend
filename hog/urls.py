from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from hog import views
from .views import contact_view, admin_messages_view

from hog.views import admin_messages_view 
urlpatterns = [
    # Public routes
    path('', views.index, name='index'),
    path('our-church/', views.our_church, name='our_church'),
    path('our-pastor/', views.our_pastor, name='our_pastor'),
    path('departments/', views.departments, name='departments'),

    
    # Department routes
    path('department/singles/', views.singles, name='singles'),
    path('department/children/', views.children, name='children'),
    path('department/works/', views.works, name='works'),
    path('department/publication/', views.publication, name='publication'),
    path('department/evangelism/', views.evangelism, name='evangelism'),
    path('department/holy-police/', views.holy, name='holy'),
    path('department/technical-crew/', views.technical, name='technical'),
    path('department/villa-sanitation/', views.villa, name='villa'),
    path('department/pastoral-care/', views.pastoral, name='pastoral'),
    path('department/missions/', views.missions, name='missions'),
    path('department/protocol/', views.protocol, name='protocol'),
    path('department/benevolence/', views.benevolence, name='benevolence'),
    
    # Fellowship and special events
    path('fellowship_sunday/january/', views.january, name='january'),
    path('Queen-Esther/2016/', views.esther16, name='esther16'),
    path('event/<slug:slug>/', views.event_public_view, name='event_detail'),
    
    # Custom admin routes
    path('custom-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/login/', views.admin_login, name='admin_login'),
    path('custom-admin/logout/', views.admin_logout, name='admin_logout'),
    path('custom-admin/event/create/', views.create_event, name='admin_create_event'),
    path('custom-admin/event/<slug:slug>/', views.event_detail, name='admin_event_detail'),
    path('custom-admin/event/<slug:slug>/edit/', views.edit_event, name='admin_edit_event'),
    path('custom-admin/event/<int:pk>/delete/', views.delete_event, name='admin_delete_event'),
    path('custom-admin/event/<slug:slug>/gallery/add/', views.add_gallery_images, name='admin_add_gallery'),
    path('custom-admin/gallery-image/<int:image_id>/delete/', views.delete_gallery_image, name='delete_gallery_image'),
    path('custom-admin/events/', views.events_list, name='events_list'),
    path('custom-admin/monthly-events/', views.monthly_events_list, name='monthly_events_list'),
    path('events/weddings/', views.weddings, name='weddings'),
     path('events/baby_dedication/', views.baby_dedication, name='baby_dedication'),
     path('events/christmas_light/', views.christmas, name='christmas_light'),
     path('media/church_gallery/', views.church_gallery, name='church_gallery'),
     path('media/pastor_gallery/', views.pastor_gallery, name='pastor_gallery'),
    
    # Monthly events routes
    path('custom-admin/monthly-events/', views.monthly_events_list, name='monthly_events_list'),
    path('custom-admin/monthly-events/create/', views.create_monthly_event, name='create_monthly_event'),
    path('custom-admin/monthly-events/<slug:slug>/', views.monthly_event_detail, name='monthly_event_detail'),
    path('custom-admin/monthly-events/<int:pk>/edit/', views.edit_monthly_event, name='edit_monthly_event'),
    path('custom-admin/monthly-events/<int:pk>/delete/', views.delete_monthly_event, name='delete_monthly_event'),
    path('custom-admin/monthly-events/<int:event_id>/gallery/add/', 
         views.add_monthly_event_gallery, 
         name='add_monthly_event_gallery'),
    path('<str:category>/<int:month>/<int:year>/', views.monthly_event_public_view, name='monthly_event_view'),
    path('monthly-events/<str:event_type>/<int:month>/', views.monthly_event_month, name='monthly_event_month'),
    
    # Monthly events public routes
    path('fellowship-sunday/<str:month>/', 
         views.monthly_event_view, 
         kwargs={'event_type': 'Fellowship Sunday'},
         name='fellowship_sunday'),
         
    path('christmas-carol/<str:month>/', 
         views.monthly_event_view,
         kwargs={'event_type': 'Christmas Carol Competition'},
         name='christmas_carol'),
         
    path('hallelujah-party/<str:month>/',
         views.monthly_event_view,
         kwargs={'event_type': 'Hallelujah Party'},
         name='hallelujah_party'),

     # Gallery admin routes
     path('custom-admin/gallery/<slug:category_slug>/', views.gallery_dashboard, name='admin_gallery'),
     path('custom-admin/gallery/<slug:category_slug>/upload/', views.add_gallery_images, name='admin_gallery_upload'),
     path('custom-admin/gallery/image/<int:image_id>/delete/', views.delete_gallery_image, name='admin_gallery_delete'),
     path('watch/', views.watch, name='watch'),
     path('custom-admin/sermons/add/', views.add_sermon, name='add_sermon'),
     path('custom-admin/sermons/<int:pk>/edit/', views.edit_sermon, name='edit_sermon'),
     path('custom-admin/sermons/<int:pk>/delete/', views.delete_sermon, name='delete_sermon'),
     path('custom-admin/sermons/', views.admin_sermon_list, name='admin_sermon_list'),
     path('sermon/<int:sermon_id>/like/', views.sermon_like, name='sermon_like'),
     path("contact/", contact_view, name="contact"),
     path("custom-admin/messages/", admin_messages_view, name="admin_messages"),
     
    path('custom-admin/messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('custom-admin/messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
    path('custom-admin/messages/<int:pk>/mark-read/', views.mark_message_as_read, name='mark_message_as_read'), 

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'hog.views.custom_404_view'
