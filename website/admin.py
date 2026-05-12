from django.contrib import admin
from .models import Service, Project, Testimonial, ContactMessage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'is_active')
    list_editable = ('is_active',)
    ordering = ('number',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'year', 'is_featured')
    ordering = ('order', '-year')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project_type', 'submitted_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'submitted_at')
    readonly_fields = ('name', 'email', 'phone', 'project_type', 'message', 'submitted_at')
    ordering = ('-submitted_at',)
