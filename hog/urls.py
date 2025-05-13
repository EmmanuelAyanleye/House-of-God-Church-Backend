from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from hog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('our-church/', views.our_church, name='our_church'),
    path('our-pastor/', views.our_pastor, name='our_pastor'),
    path('deparment/singles/', views.singles, name='singles'),
    path('deparment/children/', views.children, name='children'),
    path('deparment/works/', views.works, name='works'),
    path('deparment/publication/', views.publication, name='publication'),
    path('deparment/evangelism/', views.evangelism, name='evangelism'),
    path('deparment/holy-police/', views.holy, name='holy'),
    path('deparment/technical-crew/', views.technical, name='technical'),
    path('deparment/villa-sanitation/', views.villa, name='villa'),
    path('deparment/pastoral-care/', views.pastoral, name='pastoral'),
    path('deparment/missions/', views.missions, name='missions'),
    path('deparment/protocol/', views.protocol, name='protocol'),
    path('deparment/benevolence/', views.benevolence, name='benevolence'), 
    path('Queen-Esther/2016/', views.esther16, name='esther16'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/event/create/', views.create_event, name='admin_create_event'),
    path('admin/event/<slug:slug>/', views.event_detail, name='admin_event_detail'),
    path('admin/event/<slug:slug>/edit/', views.edit_event, name='admin_edit_event'),
    path('admin/event/<slug:slug>/gallery/add/', views.add_gallery_images, name='admin_add_gallery'),
    path('custom-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/event/create/', views.create_event, name='admin_create_event'),
    path('custom-admin/event/<slug:slug>/', views.event_detail, name='admin_event_detail'),
    path('custom-admin/event/<slug:slug>/edit/', views.edit_event, name='admin_edit_event'),
    path('custom-admin/event/<slug:slug>/gallery/add/', views.add_gallery_images, name='admin_add_gallery'),
    path('custom-admin/gallery-image/<int:image_id>/delete/', 
         views.delete_gallery_image, 
         name='delete_gallery_image'),
    path('custom-admin/login/', views.admin_login, name='admin_login'),
    path('custom-admin/logout/', views.admin_logout, name='admin_logout'),
    path('event/<slug:slug>/', views.event_public_view, name='event_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)