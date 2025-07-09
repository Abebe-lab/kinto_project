# context_processors.py
from .models import ContactInformation, Service, GoldenOpportunity

def contact_information(request):
    contact_info = ContactInformation.objects.all()
    return {
        'contact_info': contact_info
    }


def golden_opportunities(request):
    golden_count = GoldenOpportunity.objects.filter(title__icontains="Golden Opportunity").count()
    return {
        'golden_count': golden_count,
    }