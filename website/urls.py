from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', views.AboutView.as_view(), name='about'),
    path('about/', views.about_view, name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('partners/', views.PartnersView.as_view(), name='partners'),
    path('contact/', views.contact, name='contact'),
    path('submit-testimonial/', views.submit_testimonial, name='submit_testimonial'),
    path('resources/', views.resource_view, name='resources'),
    path('resources/download/<str:file_type>/<str:file_name>/', views.FileDownloadView.as_view(), name='file_download'),
    path('announcement/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)