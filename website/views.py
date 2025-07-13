# Create your views here.
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from kilinto_project import settings
from .forms import ContactForm, TestimonialForm
from .models import *
from django.http import FileResponse, Http404
from django.views import View
import os
from django.conf import settings
from django.utils._os import safe_join
from urllib.parse import unquote

def home(request):
    home_hero = HomeHero.objects.all()
    stats = QuickStat.objects.all()

    highlights = NewsArticle.objects.filter(is_highlight=True).order_by('-published_date')[:3]
    upcoming_events = Event.objects.filter(is_event=True,start_date__gte=timezone.now()).order_by('start_date')[:2]
    services = Service.objects.all()
    golden_count = services.filter(service_type='GOLDEN').count()
    context = {
        'home_hero': home_hero,
        'stats': stats,
        'highlights': highlights,
        'upcoming_events': upcoming_events,
        'services': services,
    }
    return render(request, 'website/home.html', context)

def about_view(request):
    sections = AboutSection.objects.all()
    team = ManagementTeam.objects.all()
    infrastructure = Infrastructure.objects.all()

    context = {
        'sections': sections,
        'team': team,
        'infrastructure': infrastructure,
    }
    return render(request, 'website/about.html', context)

class ServicesView(ListView):
    model = Service
    template_name = 'website/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.all().order_by('service_type', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opportunities_info = []  # List to hold opportunity info

        for opportunity in GoldenOpportunity.objects.all():
            # Calculate remaining time
            now = timezone.now()
            remaining_time = opportunity.expiry_date - now

            # Calculate months, days, and hours
            months = remaining_time.days // 30  # Approximate month calculation
            days = remaining_time.days % 30
            hours = remaining_time.seconds // 3600

            # Create a new dictionary to hold the opportunity and its remaining time
            opportunity_info = {
                'opportunity': opportunity,
                'expiry_date': opportunity.expiry_date,
                'exclusive_benefits': opportunity.exclusive_benefits.splitlines,
                'strategic_advantages': opportunity.strategic_advantages.splitlines,
                'months': months,
                'days': days,
                'hours': hours,
            }

            opportunities_info.append(opportunity_info)  # Append to the list

        context['golden_opportunities'] = opportunities_info  # Update context with the list

        return context
class NewsView(ListView):
    model = NewsArticle
    template_name = 'website/news.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = NewsArticle.objects.filter(is_highlight=True).order_by('-published_date')
        context['events'] = Event.objects.filter(is_event=True, start_date__gte=timezone.now()).order_by('start_date')
        context['media'] = MediaItem.objects.filter(is_featured=True)[:6]
        return context

class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'website/news_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'

class PartnersView(ListView):
    model = Partner
    template_name = 'website/partners.html'
    context_object_name = 'partners'

    def get_queryset(self):
        return Partner.objects.all().order_by('partner_type', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.all()
        return context

def contact(request):
    visiting_hours = VisitingHour.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(request.POST)  # Debug: Log submitted data
        if form.is_valid():
            contact_submission = form.save()
            print("Form saved successfully.")  # Debug: Confirm form save

            messages.success(request, 'Thank you for your inquiry! Your message has been submitted successfully.')
            return redirect('contact')
        else:
            print(form.errors)  # Debug: Log validation errors
    else:
        initial = {}
        # Check if there are available golden opportunities in the Service model
        if Service.objects.filter(service_type='GOLDEN').exists():
            initial = {'subject': 'GOLDEN'}  # Set subject to GOLDEN if available
        form = ContactForm(initial=initial)

    return render(request, 'website/contact.html', {'form': form, 'visiting_hours': visiting_hours})

def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your testimonial! Your submission has been received successfully.')
            return redirect('submit_testimonial')  # Redirect to the same page or a success page
    else:
        form = TestimonialForm()

    return render(request, 'website/submit_testimonial.html', {'form': form})


# Resources(announcement, downloadable and FAQs)

def resource_view(request):
    downloadables = Downloadable.objects.all()
    announcements = Announcement.objects.all()
    # announcements = Announcement.objects.filter(is_published=True, publish_date__lte=timezone.now())
    faqs = FAQ.objects.all()

    context = {
        'downloadables': downloadables,
        'announcements': announcements,
        'faqs': faqs,
    }

    return render(request, 'website/resources.html', context)

class FileDownloadView(View):

    # Mapping of file extensions to content types
    CONTENT_TYPES = {
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'mp4': 'video/mp4',
        'zip': 'application/zip',
    }

    def get(self, request, file_type, file_name, *args, **kwargs):
        try:
            # 1. Decode URL-encoded filename
            decoded_name = unquote(file_name)

            # 2. Secure path construction
            base_dir = safe_join(settings.MEDIA_ROOT, 'downloadables')
            file_path = safe_join(base_dir, decoded_name)

            # 3. Security checks
            if not self._is_valid_path(base_dir, file_path):
                raise Http404("Invalid file path")

            if not os.path.exists(file_path):
                raise Http404(f"File not found: {decoded_name}")

            if not os.path.isfile(file_path):
                raise Http404("Requested path is not a file")

            # 4. Get file info
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            last_modified = file_stat.st_mtime

            # 5. Determine content type
            content_type = self.CONTENT_TYPES.get(
                file_type.lower(),
                'application/octet-stream'
            )

            # 6. Prepare response
            response = FileResponse(
                open(file_path, 'rb'),
                content_type=content_type
            )

            # 7. Set headers
            response['Content-Disposition'] = (
                f'attachment; filename="{os.path.basename(decoded_name)}"'
            )
            response['Content-Length'] = file_size
            response['Last-Modified'] = last_modified
            response['X-Content-Type-Options'] = 'nosniff'
            response['Cache-Control'] = 'no-cache, must-revalidate'

            return response

        except (ValueError, OSError) as e:
            raise Http404("File access error") from e

    def _is_valid_path(self, base_dir, file_path):
        """Verify the resolved path is within the allowed directory"""
        # Resolve all symbolic links
        base_dir = os.path.abspath(os.path.realpath(base_dir))
        file_path = os.path.abspath(os.path.realpath(file_path))

        # Check the file is inside the base directory
        return os.path.commonpath([base_dir]) == os.path.commonpath([base_dir, file_path])
def announcement_detail(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug)
    context = {
        'announcement': announcement,
    }
    return render(request, 'website/announcement_detail.html', context)