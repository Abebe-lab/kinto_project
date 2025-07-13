from django.contrib import admin
from .models import *

@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')

# Register your models here.
@admin.register(QuickStat)
class QuickStatAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('order',)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_highlight')
    list_filter = ('published_date', 'is_highlight')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(ManagementTeam)
class ManagementTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order')
    list_editable = ('order',)

@admin.register(Infrastructure)
class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'order')
    list_filter = ('service_type',)
    list_editable = ('order',)

@admin.register(GoldenOpportunity)
class GoldenOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'exclusive_benefits', 'strategic_advantages', 'expiry_date', 'created_at')
    list_filter = ('created_at', 'expiry_date')
    search_fields = ('title', 'exclusive_benefits', 'strategic_advantages')
    ordering = ('-created_at', '-updated_at')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'joined_date', 'order')
    list_filter = ('partner_type',)
    list_editable = ('order',)
    search_fields = ('name', 'description')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('partner', 'manager_name', 'manager_role', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'partner__partner_type', 'manager_role')
    search_fields = ('partner__name', 'testimonial', 'manager_name')
    ordering = ('-is_featured', '-created_at')

    fieldsets = (
        (None, {
            'fields': ('partner', 'testimonial', 'manager_name', 'manager_role', 'is_featured')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
        return super().get_readonly_fields(request, obj)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_responded')
    list_filter = ('subject', 'is_responded', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-submitted_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'is_event')
    list_filter = ('start_date', 'is_event')
    search_fields = ('title', 'description', 'location')

@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'date_taken', 'is_featured')
    list_filter = ('media_type', 'is_featured', 'date_taken')

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('orgname', 'location', 'phone_number', 'email_address')
    list_editable = ('phone_number', 'email_address')
    search_fields = ('orgname', 'location')


# ///////////////////////////

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'is_published')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Downloadable)
class DownloadableAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_file_extension', 'upload_date', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_featured')
    list_filter = ('is_featured', 'category')
    search_fields = ('question', 'answer')

@admin.register(VisitingHour)
class VisitingHourAdmin(admin.ModelAdmin):
    list_display = ('day', 'hours', 'notes')
    search_fields = ('day',)