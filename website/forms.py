
from django import forms
from .models import ContactSubmission, Testimonial


class ContactForm(forms.ModelForm):
    # Define subject choices at the form level for easy maintenance
    SUBJECT_CHOICES = [
        ('', '--- Select Inquiry Type ---'),  # Empty/default choice
        ('GENERAL', 'General Inquiry'),
        ('GOLDEN', 'Golden Investment Opportunity (Limited Time)'),
        ('TENANCY', 'Tenancy Inquiry'),
        ('MEDIA', 'Media Inquiry'),
        ('INVESTMENT', 'Other Inquiry'),
    ]

    # Override the subject field to use our choices
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'contact-subject'  # Added ID for JavaScript targeting
        })
    )

    # Make message field required with a custom label
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Please include relevant details about your inquiry...'
        }),
        label='Your Message',
        required=True
    )

    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields automatically
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'

        # Set golden opportunity as selected if passed in initial
        if self.initial.get('subject') == 'GOLDEN':
            self.fields['subject'].widget.attrs['data-highlight'] = 'true'
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['partner', 'testimonial', 'manager_name', 'manager_role', 'is_featured']
        widgets = {
            'partner': forms.Select(attrs={
                'class': 'form-select',
                'id': 'testimonial-partner'
            }),
            'testimonial': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your testimonial here...'
            }),
            'manager_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Manager Name (Optional)'
            }),
            'manager_role': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_featured': forms.CheckboxInput(),
        }
        labels = {
            'manager_name': 'Manager Name (Optional)',
            'testimonial': 'Testimonial',
            'manager_role': 'Manager Role',
            'is_featured': 'Featured Testimonial',
        }

    def clean_testimonial(self):
        testimonial = self.cleaned_data.get('testimonial')
        if not testimonial:
            raise forms.ValidationError('Testimonial content is required.')
        return testimonial

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields automatically
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'