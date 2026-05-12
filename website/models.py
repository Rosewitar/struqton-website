from django.db import models


class Service(models.Model):
    """A structural engineering service offered by Struqton."""
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=120)
    description = models.TextField()
    icon_svg = models.TextField(blank=True, help_text="SVG path data for the service icon")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number:02d}. {self.name}"


class Project(models.Model):
    """A featured project in the portfolio."""
    CATEGORY_CHOICES = [
        ('commercial', 'Commercial'),
        ('residential', 'Residential'),
        ('industrial', 'Industrial'),
        ('mixed_use', 'Mixed-Use'),
        ('infrastructure', 'Infrastructure'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    year = models.PositiveSmallIntegerField()
    services_provided = models.CharField(max_length=300)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', '-year']

    def __str__(self):
        return self.title

    def get_category_display_color(self):
        color_map = {
            'commercial': '#1db983',
            'residential': '#1db983',
            'industrial': '#1db983',
            'mixed_use': '#1db983',
            'infrastructure': '#1db983',
        }
        return color_map.get(self.category, '#1db983')


class Testimonial(models.Model):
    """A client testimonial."""
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=150)
    quote = models.TextField()
    initials = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} — {self.client_role}"


class ContactMessage(models.Model):
    """A message submitted via the contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    project_type = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} ({self.email}) — {self.submitted_at:%Y-%m-%d}"
