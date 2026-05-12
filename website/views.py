"""
Views for the Struqton Structural website.

Routes
------
/                       -> index (prototype gallery / landing)
/prototype/1/           -> Precision Dark
/prototype/2/           -> Authority Gold
/prototype/3/           -> Clarity Light
/prototype/4/           -> Cinematic
/prototype/5/           -> Industrial Bold
/contact/               -> Contact form (POST handler)
/contact/success/       -> Thank-you page after form submission
"""

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import ContactForm
from .models import Service, Project, Testimonial

# ---------------------------------------------------------------------------
# Shared site context
# ---------------------------------------------------------------------------

SITE_DATA = {
    'company_name': 'Struqton Structural',
    'tagline': 'Built on Precision. Designed to Last.',
    'email': 'info@struqton.com',
    'phone': '+263 000 000 000',
    'address': 'Harare, Zimbabwe',
    'website': 'struqtonstructural.com',
    'stats': {
        'projects': '120+',
        'years': '8+',
        'provinces': '3',
        'on_spec': '100%',
    },
    'services': [
        {
            'number': '01',
            'name': 'Structural Design',
            'description': (
                'We transform architectural visions into safe, durable realities. '
                'Full structural analysis for buildings of all scales — residential, '
                'commercial, and mixed-use — with comprehensive drawings and '
                'calculations compliant with local codes.'
            ),
        },
        {
            'number': '02',
            'name': 'Construction Supervision',
            'description': (
                'On-site engineering oversight ensuring every phase of construction '
                'meets the approved structural design. We catch issues early and keep '
                'your build on specification and on schedule.'
            ),
        },
        {
            'number': '03',
            'name': 'Building Inspections',
            'description': (
                'Structural assessments for existing buildings, extensions, and '
                'renovations. Formal inspection reports, compliance certificates, '
                'and structural opinions for financial or legal purposes.'
            ),
        },
        {
            'number': '04',
            'name': 'Foundation Engineering',
            'description': (
                'Geotechnical assessments and foundation design tailored to '
                "Zimbabwe's varied soil conditions. Strip, raft, pad, and pile "
                'foundations — safe, economical, and code-compliant.'
            ),
        },
        {
            'number': '05',
            'name': 'Steel Frame Design',
            'description': (
                'Custom steel structures for industrial, commercial, and specialised '
                'applications. Optimised for material efficiency, fabrication, and '
                'long-term structural integrity.'
            ),
        },
        {
            'number': '06',
            'name': 'Reports & Compliance',
            'description': (
                'Formal structural reports for building permits, insurance, mortgage '
                'applications, and regulatory submissions. Clear documentation '
                'prepared by registered engineers.'
            ),
        },
    ],
    'projects': [
        {
            'title': 'Commercial Complex — Harare CBD',
            'category': 'Commercial',
            'services': 'Structural design & construction supervision',
            'year': 2024,
            'color_class': 'pi-a',
        },
        {
            'title': 'Residential Estate — Borrowdale',
            'category': 'Residential',
            'services': 'Foundation engineering & structural package',
            'year': 2023,
            'color_class': 'pi-b',
        },
        {
            'title': 'Industrial Warehouse — Msasa',
            'category': 'Industrial',
            'services': 'Steel frame design & supervision',
            'year': 2023,
            'color_class': 'pi-c',
        },
        {
            'title': 'Mixed-Use Development — Avondale',
            'category': 'Mixed-Use',
            'services': 'Full structural engineering package',
            'year': 2024,
            'color_class': 'pi-d',
        },
    ],
    'testimonials': [
        {
            'initials': 'TM',
            'name': 'Takudzwa Mhiripiri',
            'role': 'Property Developer, Harare',
            'quote': (
                'Struqton delivered our structural package faster than any firm '
                "we'd worked with before — and the quality was exceptional. "
                "We'll be using them on every future development."
            ),
        },
        {
            'initials': 'SN',
            'name': 'Simba Ndlovu',
            'role': 'Site Manager, Bulawayo',
            'quote': (
                'Their on-site supervision caught a critical foundation issue early. '
                'That intervention alone saved us weeks of delays and significant '
                'remediation costs.'
            ),
        },
        {
            'initials': 'FK',
            'name': 'Farai Kachingwe',
            'role': 'Homeowner, Borrowdale',
            'quote': (
                'The compliance report Struqton prepared got our building permit '
                'approved first time. Professional, thorough, and they explained '
                'everything clearly throughout.'
            ),
        },
    ],
}

# Prototype metadata for the landing page gallery
PROTOTYPES = [
    {
        'id': 1,
        'slug': 'precision-dark',
        'name': 'Precision Dark',
        'palette': 'Navy + Emerald Green',
        'description': (
            'Data-forward dark theme with emerald accents. Features a stats panel hero, '
            'animated scroll progress bar, service grid, and client testimonials section.'
        ),
        'bg': '#08111e',
        'accent': '#1db983',
        'font': 'Syne + DM Sans',
    },
    {
        'id': 2,
        'slug': 'authority-gold',
        'name': 'Authority Gold',
        'palette': 'Black + Gold',
        'description': (
            'Editorial luxury feel with Cormorant Garamond serif. Numbered service list, '
            'gold stats band, and manifesto-style about section.'
        ),
        'bg': '#070707',
        'accent': '#c8a84b',
        'font': 'Cormorant Garamond + Inter',
    },
    {
        'id': 3,
        'slug': 'clarity-light',
        'name': 'Clarity Light',
        'palette': 'Cream + Navy',
        'description': (
            'Clean, corporate B2B design on a light background. Includes a 4-step Process '
            'section and trust indicators — ideal for institutional clients.'
        ),
        'bg': '#f7f5f0',
        'accent': '#1565a0',
        'font': 'Plus Jakarta Sans',
    },
    {
        'id': 4,
        'slug': 'cinematic',
        'name': 'Cinematic',
        'palette': 'Black + Amber',
        'description': (
            'Dramatic full-viewport hero with Bebas Neue display type. Horizontal '
            'service list and project strips — inspired by "show, don\'t tell" design.'
        ),
        'bg': '#06080a',
        'accent': '#e07b2a',
        'font': 'Bebas Neue + Inter',
    },
    {
        'id': 5,
        'slug': 'industrial-bold',
        'name': 'Industrial Bold',
        'palette': 'Charcoal + Yellow',
        'description': (
            'High-energy construction industry aesthetic. Split hero, animated yellow '
            'ticker, and dense service grid with strong yellow accent throughout.'
        ),
        'bg': '#141414',
        'accent': '#f5c518',
        'font': 'Space Grotesk',
    },
]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def index(request):
    """Landing page — prototype gallery."""
    context = {
        'prototypes': PROTOTYPES,
        'site': SITE_DATA,
        'page_title': 'Struqton Structural — Design Prototypes',
    }
    return render(request, 'website/index.html', context)


def prototype(request, prototype_id):
    """Render a specific design prototype by ID (1–5)."""
    if prototype_id not in range(1, 6):
        raise Http404("Prototype not found.")

    # Find prototype metadata
    proto_meta = next((p for p in PROTOTYPES if p['id'] == prototype_id), None)

    context = {
        'site': SITE_DATA,
        'proto': proto_meta,
        'page_title': f"Struqton — {proto_meta['name']} Prototype",
        # Pass form for the contact section
        'contact_form': ContactForm(),
    }
    template_name = f'website/prototype_{prototype_id}.html'
    return render(request, template_name, context)


@require_http_methods(['POST'])
def contact_submit(request):
    """Handle contact form POST submissions."""
    form = ContactForm(request.POST)
    # Determine which prototype the form was submitted from (for redirect back)
    source_proto = request.POST.get('source_prototype', '1')

    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Thank you! We've received your message and will be in touch within 24 hours."
        )
        return redirect('contact_success')

    # Re-render the prototype with form errors
    try:
        proto_id = int(source_proto)
    except (ValueError, TypeError):
        proto_id = 1

    proto_meta = next((p for p in PROTOTYPES if p['id'] == proto_id), PROTOTYPES[0])
    context = {
        'site': SITE_DATA,
        'proto': proto_meta,
        'page_title': f"Struqton — {proto_meta['name']} Prototype",
        'contact_form': form,
    }
    return render(request, f'website/prototype_{proto_id}.html', context)


def contact_success(request):
    """Thank-you page after form submission."""
    context = {
        'site': SITE_DATA,
        'page_title': 'Message Received — Struqton Structural',
    }
    return render(request, 'website/contact_success.html', context)
