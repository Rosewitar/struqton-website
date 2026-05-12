from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact / enquiry form for the Struqton website."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'project_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+263 ...',
                'class': 'form-input',
            }),
            'project_type': forms.Select(
                choices=[
                    ('', 'Select a service…'),
                    ('structural_design', 'Structural Design'),
                    ('construction_supervision', 'Construction Supervision'),
                    ('building_inspection', 'Building Inspection'),
                    ('foundation_engineering', 'Foundation Engineering'),
                    ('steel_frame_design', 'Steel Frame Design'),
                    ('compliance_report', 'Reports & Compliance'),
                    ('other', 'Other / Not sure yet'),
                ],
                attrs={'class': 'form-select'},
            ),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project…',
                'rows': 5,
                'class': 'form-textarea',
            }),
        }
        labels = {
            'phone': 'Phone (optional)',
            'project_type': 'Service required',
        }
