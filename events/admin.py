from django.contrib import admin
from .models import Event, Registration, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'venue', 'price', 'organizer')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('organizer', 'category')
    search_fields = ('title', 'venue')
    inlines = [RegistrationInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'created_at')
    list_filter = ('event',)
    search_fields = ('full_name', 'email', 'event__title')
