from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

class HomeHero(models.Model):
    COLOR_CHOICES = [
        ('WHITE', 'White'),
        ('BLACK', 'Black'),
        ('GREEN', 'Green'),
        ('BROWN', 'Brown'),
    ]
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='HomeImages/')
    color_type = models.CharField(max_length=20, choices=COLOR_CHOICES, default='null')


    def __str__(self):
        return self.title

class QuickStat(models.Model):
    ICON_CHOICES = [
        ('bi bi-building', 'Company'),
        ('bi bi-map', 'Land Size'),
        ('bi bi-briefcase', 'Jobs'),
    ]
    icon_type = models.CharField(max_length=20, choices=ICON_CHOICES, default='COMPANY')
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    description = RichTextField(default='none')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_highlight = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    ICON_CHOICES = [
        ('bi bi-building', 'Park'),
        ('bi bi-bullseye', 'Mission'),
        ('bi bi-eye-fill', 'Vision'),
    ]
    icon_type = models.CharField(max_length=20, choices=ICON_CHOICES, default='Park')
    title = models.CharField(max_length=200)
    content = RichTextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ManagementTeam(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.position}"

class Infrastructure(models.Model):
    ICON_CHOICES = [
        ('fas fa-bolt', 'Power Supply'),
        ('fas fa-tint', 'Water System'),
        ('fas fa-trash-alt', 'Waste Management'),
    ]
    icon_type = models.CharField(max_length=100, choices=ICON_CHOICES, default='Power Supply')
    title = models.CharField(max_length=200)
    description = RichTextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
class Service(models.Model):
    SERVICE_TYPES = [
        ('FACILITY', 'Business Facilities'),
        ('SUPPORT', 'Support Services'),
        ('INVESTMENT', 'Investment Opportunities'),
        # ('GOLDEN', 'Golden Investment Opportunities'),
    ]

    ICON_CHOICES = [
        ('bi bi-building', 'Business Facilities'),
        ('bi bi-people', 'Support Services'),
        ('bi bi-wallet', 'Investment Opportunities'),
        # ('bi bi-gem', 'Golden Investment Opportunities'),
    ]
    icon_type = models.CharField(max_length=100, choices=ICON_CHOICES, default='Business Facilities')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='Golden Investment Opportunities')
    title = models.CharField(max_length=200)
    description = RichTextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class GoldenOpportunity(models.Model):
    title = models.CharField(max_length=255, default="Golden Opportunity")
    exclusive_benefits = models.TextField()
    strategic_advantages = models.TextField()
    expiry_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Partner(models.Model):
    PARTNER_TYPES = [
        ('PARTNER', 'Partner'),
        ('TENANT', 'Tenant'),
        ('INVESTOR', 'Investor'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=200)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES)
    logo = models.ImageField(upload_to='partners/')
    description = models.TextField()
    website = models.URLField(blank=True)
    joined_date = models.DateField()
    # testimonial = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('Manager', 'Manager'),
        ('Director', 'Director'),
        ('Other', 'Other'),
    ]

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='testimonials')
    testimonial = models.TextField(blank=True, help_text="The testimonial text content")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager_name = models.CharField(max_length=100, blank=True, default="")
    manager_role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, default="")

    def clean(self):
        super().clean()
        if not self.testimonial:
            raise ValidationError('Testimonial content is required.')

    def __str__(self):
        return f"{self.manager_name} - Testimonial"

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
# Contact Submission Model
class ContactSubmission(models.Model):
    SUBJECT_CHOICES = [
        ('INVESTMENT', 'Investment Inquiry'),
        ('TENANCY', 'Tenancy Inquiry'),
        ('GOLDEN', 'Golden Investment Opportunities'),
        ('GENERAL', 'General Inquiry'),
        ('MEDIA', 'Media Inquiry'),
        ('OTHER', 'Other Inquiry'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='events/', blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_event = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class MediaItem(models.Model):
    MEDIA_TYPES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    date_taken = models.DateField()
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class ContactInformation(models.Model):
    orgname = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length = 500, blank=True, null=True)
    phone_number = models.CharField(max_length = 15, blank=True, null=True)
    email_address = models.EmailField(max_length = 15, blank=True, null=True)
    def __str__(self):
        return self.orgname

class ResourceCategory(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Resource Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Announcement(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Additional fields
    image = models.ImageField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    docs = models.FileField(blank=True)
    expired = models.BooleanField(default=False)
    starting_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[self.slug])
class Downloadable(models.Model):
    """Model for files users can download (PDFs, Docs, etc.)"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='downloadables/')
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.title

    def get_file_extension(self):
        return self.file.name.split('.')[-1].upper()

    def get_absolute_url(self):
        return reverse('downloadable_detail', args=[self.slug])

class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

# visiting hours
class VisitingHour(models.Model):
    day = models.CharField(max_length=50)
    hours = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.day